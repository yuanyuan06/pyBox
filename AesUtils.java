import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.UnsupportedEncodingException;
import java.nio.charset.StandardCharsets;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;


public class AesUtils {
    private static final byte[] IV_BYTES = "0102030405060708".getBytes();
    private static final char[] CA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".toCharArray();

    private static String base64Encode(byte[] src) {
        byte[] res = encodeToByte(src, false);
        return src != null ? new String(res, StandardCharsets.UTF_8) : null;

    }

    private static byte[] encodeToByte(byte[] sArr, boolean lineSep) {
        int sLen = sArr != null ? sArr.length : 0;
        if (sLen == 0) {
            return new byte[0];
        } else {
            int eLen = sLen / 3 * 3;
            int cCnt = (sLen - 1) / 3 + 1 << 2;
            int dLen = cCnt + (lineSep ? (cCnt - 1) / 76 << 1 : 0);
            byte[] dArr = new byte[dLen];
            int left = 0;
            int d = 0;
            int cc = 0;

            while (left < eLen) {
                int i = (sArr[left++] & 255) << 16 | (sArr[left++] & 255) << 8 | sArr[left++] & 255;
                dArr[d++] = (byte) CA[i >>> 18 & 63];
                dArr[d++] = (byte) CA[i >>> 12 & 63];
                dArr[d++] = (byte) CA[i >>> 6 & 63];
                dArr[d++] = (byte) CA[i & 63];
                if (lineSep) {
                    ++cc;
                    if (cc == 19 && d < dLen - 2) {
                        dArr[d++] = 13;
                        dArr[d++] = 10;
                        cc = 0;
                    }
                }
            }

            left = sLen - eLen;
            if (left > 0) {
                d = (sArr[eLen] & 255) << 10 | (left == 2 ? (sArr[sLen - 1] & 255) << 2 : 0);
                dArr[dLen - 4] = (byte) CA[d >> 12];
                dArr[dLen - 3] = (byte) CA[d >>> 6 & 63];
                dArr[dLen - 2] = left == 2 ? (byte) CA[d & 63] : 61;
                dArr[dLen - 1] = 61;
            }
            return dArr;
        }
    }

    public String aesUtil(String key, String content)throws NoSuchAlgorithmException, NoSuchPaddingException, BadPaddingException, IllegalBlockSizeException, InvalidAlgorithmParameterException, InvalidKeyException, UnsupportedEncodingException
    {
        byte[] bytes = key.getBytes();
        byte[] content_bytes = content.getBytes();

        SecureRandom random = SecureRandom.getInstance("SHA1PRNG");
        random.setSeed(bytes);
        KeyGenerator kgen = KeyGenerator.getInstance("AES");
        kgen.init(256, random);
        SecretKey secretKey = kgen.generateKey();
        IvParameterSpec iv = new IvParameterSpec(IV_BYTES);
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(secretKey.getEncoded(), "AES"), iv);
        return base64Encode(cipher.doFinal(content_bytes));
    }
}