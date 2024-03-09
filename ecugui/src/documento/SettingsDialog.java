package documento;

public class SettingsDialog extends javax.swing.JDialog {

	@SuppressWarnings("unchecked")
  // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
  private void initComponents() {

    settingsPanel = new documento.SettingsPanel();

    setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE);
    getContentPane().add(settingsPanel, java.awt.BorderLayout.CENTER);

    pack();
  }// </editor-fold>//GEN-END:initComponents

	public static void main (String args[]) {
		/*
		 * Set the Nimbus look and feel
		 */
		//<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
		/*
		 * If Nimbus (introduced in Java SE 6) is not available, stay with the
		 * default look and feel. For details see
		 * http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html
		 */
		try {
			for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels ()) {
				if ("Nimbus".equals (info.getName ())) {
					javax.swing.UIManager.setLookAndFeel (info.getClassName ());
					break;
				}
			}
		} catch (ClassNotFoundException ex) {
			java.util.logging.Logger.getLogger (SettingsDialog.class.getName ()).log (java.util.logging.Level.SEVERE, null, ex);
		} catch (InstantiationException ex) {
			java.util.logging.Logger.getLogger (SettingsDialog.class.getName ()).log (java.util.logging.Level.SEVERE, null, ex);
		} catch (IllegalAccessException ex) {
			java.util.logging.Logger.getLogger (SettingsDialog.class.getName ()).log (java.util.logging.Level.SEVERE, null, ex);
		} catch (javax.swing.UnsupportedLookAndFeelException ex) {
			java.util.logging.Logger.getLogger (SettingsDialog.class.getName ()).log (java.util.logging.Level.SEVERE, null, ex);
		}
		//</editor-fold>
		//</editor-fold>

		/*
		 * Create and display the dialog
		 */
		java.awt.EventQueue.invokeLater (new Runnable () {
			public void run () {
				SettingsDialog dialog = new SettingsDialog (new javax.swing.JFrame (), true);
				dialog.addWindowListener (new java.awt.event.WindowAdapter () {
					@Override
					public void windowClosing (java.awt.event.WindowEvent e) {
						System.exit (0);
					}
				});
				dialog.setVisible (true);
			}
		});
	}

  // Variables declaration - do not modify//GEN-BEGIN:variables
  private documento.SettingsPanel settingsPanel;
  // End of variables declaration//GEN-END:variables

	SettingsController controller;

	/**
	 * Creates new form SettingsConfigDialog
	 */
	public SettingsDialog (java.awt.Frame parent, boolean modal) {
		super (parent, modal);
		initComponents ();
	}

	public void setController (SettingsController controller) {
		this.controller = controller;
		this.settingsPanel.setController (controller);
	}
	
	public String getCompanyName () {
		return this.settingsPanel.getEmpresaField().getText ();
	}
	public String getDocsCreatorURL () {
		return this.settingsPanel.getCreadorField().getText ();
	}
	public String getEcuapassURL () {
		return this.settingsPanel.getEcuapassField().getText ();
	}
	
	public void setCreadorField (String creadorField) {
		this.settingsPanel.setCreadorField (creadorField);
	}

	public void setEcuapassField (String ecuapassField) {
		this.settingsPanel.setEcuapassField (ecuapassField);
	}

	public void setEmpresaField (String empresaField) {
		this.settingsPanel.setEmpresaField (empresaField);
	}

}
