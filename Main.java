import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Test test = new Test();
        test.sendUDPStuff();
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                // TODO Auto-generated method stub
                test.getUDPData();
            }
        });
        thread.start();
        Scanner sc = new Scanner(System.in);
        String stuff = sc.nextLine();
    }
}
