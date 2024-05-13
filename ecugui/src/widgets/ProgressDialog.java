package widgets;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

// Creates a dialog for waiting to finish or cancel the document processing
public class ProgressDialog {
	private static final int DIALOG_WIDTH = 300;
	private static final int DIALOG_HEIGHT = 150;
	private static final int TIMER_DELAY = 1000; // 1 second

	private JFrame mainFrame;
	private JDialog progressDialog;
	private JLabel messageLabel;
	private JLabel timerLabel;
	private JButton cancelButton;
	private int elapsedTime = 0;
	private Timer timer;

	public ProgressDialog (JFrame mainFrame) {
		this.mainFrame = mainFrame;
	}

	public void startProcess () {
		//mainFrame.setEnabled (false);

		progressDialog = new JDialog (mainFrame, "Analizando documentos...", Dialog.ModalityType.APPLICATION_MODAL);
		progressDialog.setSize (DIALOG_WIDTH, DIALOG_HEIGHT);
		progressDialog.setResizable (false);
		progressDialog.setLocationRelativeTo(mainFrame);
		progressDialog.setLayout (new BorderLayout ());

		messageLabel = new JLabel ("Analizando documentos...");
		timerLabel = new JLabel ("Tiempo transcurrido: 0 segundos");
		cancelButton = new JButton ("Cancelar");
		cancelButton.addActionListener (e -> endProcess ("cancel_event"));

		JPanel panel = new JPanel (new FlowLayout ());
		panel.add (messageLabel);

		JPanel timerPanel = new JPanel (new FlowLayout ());
		timerPanel.add (timerLabel);

		JPanel buttonPanel = new JPanel (new FlowLayout ());
		buttonPanel.add (cancelButton);

		progressDialog.add (panel, BorderLayout.NORTH);
		progressDialog.add (timerPanel, BorderLayout.CENTER);
		progressDialog.add (buttonPanel, BorderLayout.SOUTH);

		timer = new Timer (TIMER_DELAY, new ActionListener () {
			@Override
			public void actionPerformed (ActionEvent e) {
				elapsedTime++;
				timerLabel.setText ("Tiempo transcurrido: " + elapsedTime + " seconds");
			}
		});
		timer.start ();

		progressDialog.setVisible (true);
	}

	public void endProcess (String actionType) {
		if (actionType.equals ("document_processed") ||
			actionType.equals ("cancel_event")) {
			timer.stop ();
			progressDialog.dispose ();
			mainFrame.setEnabled (true);
		}
	}

	public static void main (String[] args) {
		JFrame mainFrame = new JFrame ("GUI App");
		mainFrame.setDefaultCloseOperation (JFrame.EXIT_ON_CLOSE);

		mainFrame.getContentPane ().setLayout (new FlowLayout ());

		JButton startButton = new JButton ("Start Process");
		ProgressDialog pd = new ProgressDialog (mainFrame);
		startButton.addActionListener (e -> pd.startProcess ());

		mainFrame.getContentPane ().add (startButton);
		mainFrame.setSize (400, 100);
		mainFrame.setVisible (true);

	}
}
