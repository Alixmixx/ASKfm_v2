import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public final class Signature {
    public static final Signature INSTANCE = new Signature();

    private Signature() {
    }

    public final String generateHash(String str, String str2, String str3, Map<String, ? extends Object> map) {
        String apiPrivateKey = "CE2766AA8B74FBAC70A26CF5C83E9";
        return generateHashWithKey(apiPrivateKey, str, str2, str3, map);
    }

    public static final String generateHashWithKey(String str, String str2, String str3, String str4, Map<String, ? extends Object> map) {
        try {
            return sha1(str2 + '%' + str3 + '%' + str4 + '%' + INSTANCE.serializeParams(map), str);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public static final String sha1(String str, String str2) throws Exception {
        Mac instance = Mac.getInstance("HmacSHA1");
        Charset charset = Charset.forName("UTF-8");
        byte[] bytes = str2.getBytes(charset);
        instance.init(new SecretKeySpec(bytes, "HmacSHA1"));
        byte[] bytes2 = str.getBytes(charset);
        byte[] doFinal = instance.doFinal(bytes2);
        StringBuffer stringBuffer = new StringBuffer(doFinal.length * 2);
        for (byte appendHex : doFinal) {
            INSTANCE.appendHex(stringBuffer, appendHex);
        }
        String stringBuffer2 = stringBuffer.toString();
        Locale locale = Locale.US;
        String lowerCase = stringBuffer2.toLowerCase(locale);
        return lowerCase;
    }

    private final void appendHex(StringBuffer stringBuffer, byte b) {
        stringBuffer.append("0123456789ABCDEF".charAt((b >> 4) & 15));
        stringBuffer.append("0123456789ABCDEF".charAt(b & 15));
    }

    private final String serializeParams(Map<String, ? extends Object> map) {
        ArrayList<String> arrayList = new ArrayList<>();
        for (Map.Entry<String, ? extends Object> entry : map.entrySet()) {
            String key = entry.getKey();
            Object value = entry.getValue();
            if (value != null) {
                arrayList.add(encode(key) + '%' + encode(value.toString()).replace("+", "%20"));
            }
        }
        Collections.sort(arrayList);
        return concatenateList(arrayList, "%");
    }

    private final String concatenateList(List<String> list, String str) {
        if (list.isEmpty()) {
            return "";
        }
        StringBuilder sb = new StringBuilder(list.get(0));
        int size = list.size();
        for (int i = 1; i < size; i++) {
            sb.append(str);
            sb.append(list.get(i));
        }
        String sb2 = sb.toString();
        return sb2;
    }

    public static final String encode(String str) {
        if (str == null) {
            return "";
        }
        try {
            String encoded = URLEncoder.encode(str, StandardCharsets.UTF_8.name());
            encoded = encoded.replace("+", "%20");
            encoded = encoded.replace("%21", "!");
            encoded = encoded.replace("%27", "'");
            encoded = encoded.replace("%28", "(");
            encoded = encoded.replace("%29", ")");
            encoded = encoded.replace("%7E", "~");
            return encoded;
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
            return null;
        }   
    }
}
