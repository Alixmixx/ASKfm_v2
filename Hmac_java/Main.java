import java.util.HashMap;
import java.util.Map;

public class Main {

    public static void main(String[] args) {

        Map argsMap = new HashMap();
        for (int i = 3; i < args.length; i+=2) {
            argsMap.put(args[i], args[i + 1]);
        }
        try {
            System.out.println(Signature.INSTANCE.generateHash(args[0], args[1], args[2], argsMap));
        } catch (Exception e) {
            e.printStackTrace();
        }    
    }
}