package documento;

public class SettingsDialog extends javax.swing.JDialog {

	@SuppressWarnings("unchecked")
  // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
  private void initComponents() {

    settingsPanel = new documento.SettingsPanel();

    setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE);

    settingsPanel.setToolTipText("");
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

	public SettingsDialog (java.awt.Frame parent, boolean modal) {
		super (parent, modal);
		initComponents ();

		settingsPanel.getCompanyField ().setText (DocModel.companyName);
		settingsPanel.getEcuapassdocsField ().setText (DocModel.ecuapassdocsURL);
		settingsPanel.getCodebiniField ().setText (DocModel.codebiniURL);
		settingsPanel.getEcuapassField ().setText (DocModel.ecuapassURL);
	}

	public void setController (SettingsController controller) {
		this.controller = controller;
		this.settingsPanel.setController (controller);
	}

	public String getNombreEmpresa () {
		return this.settingsPanel.getCompanyField ().getText ();
	}

	public String getEcuapassdocsURL () {
		return this.settingsPanel.getEcuapassdocsField ().getText ();
	}

	public String getCodebiniURL () {
		return this.settingsPanel.getCodebiniField ().getText ();
	}

	public String getEcuapassURL () {
		return this.settingsPanel.getEcuapassField ().getText ();
	}

	public void setCompanyName (String empresaField) {
		this.settingsPanel.getCompanyField ().setText (empresaField);
	}

	public void setEcuapassdocsURL (String ecuapassdocsURL) {
		this.settingsPanel.getEcuapassdocsField ().setText (ecuapassdocsURL);
	}

	public void setCodebiniURL (String codebiniURL) {
		this.settingsPanel.getCodebiniField ().setText (codebiniURL);
	}

	public void setEcuapassURL (String ecuapassField) {
		this.settingsPanel.getEcuapassField ().setText (ecuapassField);
	}
}
