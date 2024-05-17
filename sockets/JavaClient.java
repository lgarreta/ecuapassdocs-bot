import java.io.*;
import java.net.*;

public class JavaClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 8888);
            OutputStream out = socket.getOutputStream();
            PrintWriter writer = new PrintWriter(out, true);
            
            // Send request to Python server
            writer.println("REQUEST ARG1 ARG2");
            
            // Receive response from Python server
            InputStream in = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(in));
            String response = reader.readLine();
            System.out.println("Response from Python server: " + response);
            
            // Close resources
            writer.close();
            reader.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

