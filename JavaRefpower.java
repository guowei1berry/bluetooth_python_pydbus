import java.io.*;

public class JavaRefpower 
{
private static double calculateAccuracy(
    int rssi,
    int measuredPower
) {
    int RSSI = Math.abs(rssi);

    if (RSSI == 0.0D) {
        return -1.0D;
    }

    double ratio = RSSI * 1.0D / measuredPower;
    if (ratio < 1.0D) {
        return Math.pow(
            ratio,
            8.0D
        );
    }

    return 0.69976D * Math.pow(
        ratio,
        7.7095D
    ) + 0.111D;
    
}

public static void main(String[] args) {
System.out.println(calculateAccuracy(-47,197)); //1.0496706504699393E-5 as answer

}

}

