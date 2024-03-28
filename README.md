# AskFM-POC
AskFM OSINT Proof of concept

## Introduction

While trying to find some fun way to use the app, I found out that the Add Friends option could be of some use.
In fact, it works in a way that i did not expect. While all your private informations are "private" and should not be visible on your profile,
somehow, you can do a research using an email and it will return you the linked profile. Pretty interesting.
I'm going to try to find a way to use this functionality outside the app and in a scalable way.
Also worth mentioning, you don't need to be registered to use this functionality.

## Network Analysis

So first of all, I wanted to find how the app comunicate with the ASKFM server, so i started a network analysis.
Here is what a regular request looks like

```
GET https://api.ask.fm/search?bio=miaooo&limit=25&name=miaooo&offset=0&rt=29&ts=1709016214 HTTP/1.1
Host: api.ask.fm
X-Access-Token: .3tzAQ2JtaZ2G5GKp77BQv7fJkOt2E
X-Api-Version: 1.18
Connection: keep-alive
X-Client-Type: ios_4.89.5
Accept: */*
Accept-Language: en-US,en;q=0.9
Authorization: HMAC FAC9BF579D474290AF2C67F6732688B805FD1897
Accept-Encoding: gzip, deflate, br
User-Agent: askfm/4535 CFNetwork/1492.0.1 Darwin/23.3.0
```

Most of the headers are not really important, and as long as we don't change them, everything will be fine.
The two interesting ones are the 'X-Access-Token' and the 'Authorization'

### X-Access-Token
This access token seems to be realated to a session with the server. This is the first thing we need.
As soon as a connection is established with the server, the app send a GET request to api.ask.fm/token
with some device related parameters, and a response will be returned with a accessToken that will be used 
in every request for this session.

![TokenHeader](https://github.com/Alixmixx/AskFM-POC/blob/main/images/TokenHeader.png?raw=true)

### Authorization
This authorization is a little more tricky, as it is constantly changing with every request. It seems like a
hash of some sort. In order to understand this one, i found no other way than to start reversing the app.
After finding some intersting strings inside, I decompiled the apk to start looking for this HMAC function.
I quickly found this java file that does all the computation to calculate the hash for each request.
It uses the method, host, path, params and a key.


![GenerateHash](https://github.com/Alixmixx/AskFM-POC/blob/main/images/GenerateHash.png?raw=true)

It calls some other functions to calculate the hash and uses an apiKey, so I started looking for the key.
I found this line which looked like a key, and was really happy at first

![Setup](https://github.com/Alixmixx/AskFM-POC/blob/main/images/Setup.png?raw=true)

But after a better look, I found out the KeyGenerator class was implemented inside a shared library
Sadly, even after some time looking at the objdump of that library, i couldn't find what this clientKey function
was doing exactly, as this library was calling some global variables from other libraries :(

![KeyGenerator](https://github.com/Alixmixx/AskFM-POC/blob/main/images/KeyGenerator.png?raw=true)

```
❯ readelf -d libffmpcodec.so

Dynamic section at offset 0xbc8 contains 27 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [liblog.so]
 0x0000000000000001 (NEEDED)             Shared library: [libm.so]
 0x0000000000000001 (NEEDED)             Shared library: [libdl.so]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so]
 0x000000000000000e (SONAME)             Library soname: [libffmpcodec.so]
 ```

I also found out that those libraries are on Android, so i couldn't compile a simple Java program that
called this function to find the behavior, it had to be in an app.
So at this point I just decided to decompile the app, add some logs just after the use of this function
and then align, sign and recompile the app.
Was not an easy task but I managed to get a result

Added this line to the Signature.smali file just after the getApiPrivateKey call

```
const-string v2, "TheKey"

invoke-static {v2, v0}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
```

Some commands to recompile the app
```
apktool d -f ask-fm-4-91-1.apk -o newapktest
code newapktest
apktool b -f -d newapktest
keytool -genkey -v -keystore my.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias app\
~/Library/Android/sdk/build-tools/28.0.3/zipalign -p 4 newapktest/dist/ask-fm-4-91-1.apk newapktest/dist/aligned.apk
~/Library/Android/sdk/build-tools/28.0.3/zipalign -v -c 4 newapktest/dist/aligned.apk
~/Library/Android/sdk/build-tools/28.0.3/apksigner sign --ks-key-alias app --ks my.keystore newapktest/dist/aligned.apk
~/Library/Android/sdk/build-tools/28.0.3/apksigner verify newapktest/dist/aligned.apk
```

And we are ready to launch our new modified app. (Almost, after some android studio configuration to find the right SDK and emualted phone)

![TheKey](https://github.com/Alixmixx/AskFM-POC/blob/main/images/TheKey.png?raw=true)

And here is our not so private apiPrivateKey.

I also made some other logs in order to make sure of the parameters that are given to the hash function and the output hash

![HashArgs](https://github.com/Alixmixx/AskFM-POC/blob/main/images/HashArgs.png?raw=true)

With that in mind, I started to make some python scripts to send requests to the server and implement the hash function

