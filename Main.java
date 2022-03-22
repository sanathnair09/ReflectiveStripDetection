
public class Main {
    public static void main(String[] args) {
        System.out.println("stuff working");
        Test test = new Test();
        // test.sendUDPStuff();
        while (true) {
            test.getUDPData();
        }
    }
}
