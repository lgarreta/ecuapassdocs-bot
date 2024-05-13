
import java.io.File;
import java.net.URLConnection;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author lg
 */
public class TestFileContentType {
	public void whenUsingGuessContentTypeFromName_thenSuccess () {
		//File file = new File ("/home/lg/AAA/factura-oxxo.jpg");
		// File file = new File ("/home/lg/AAA/factura-CablePlaza.png");
		File file = new File ("/home/lg/AAA/factura-CifuentesHermanos.tif");
		String mimeType = URLConnection.guessContentTypeFromName (file.getName ());
		System.out.println (mimeType);

		//assertEquals (mimeType, "image/png");
	}
	public static void main(String args[]) {
		new TestFileContentType ().whenUsingGuessContentTypeFromName_thenSuccess ();
	}

}
