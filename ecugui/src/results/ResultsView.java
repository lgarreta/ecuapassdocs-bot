package results;

import main.FileSelectionTable;
import main.Controller;
import widgets.ImageViewLens;
import java.awt.BorderLayout;

public class ResultsView extends javax.swing.JPanel {
	@SuppressWarnings("unchecked")
  // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
  private void initComponents() {

    splitImage = new javax.swing.JSplitPane();
    splitFiles = new javax.swing.JSplitPane();
    fileSelectionTable = new main.FileSelectionTable();
    recordPanel = new javax.swing.JPanel();
    transmitControlPanel = new javax.swing.JPanel();
    sendEcuapassButton = new javax.swing.JButton();
    sendCodebinButton = new javax.swing.JButton();
    ecuapassView = new results.EcuapassView();
    imageView = new widgets.ImageViewLens();

    setBorder(javax.swing.BorderFactory.createLineBorder(new java.awt.Color(0, 0, 0)));
    setLayout(new java.awt.BorderLayout());

    splitImage.setBackground(new java.awt.Color(204, 204, 255));
    splitImage.setMinimumSize(new java.awt.Dimension(732, 400));

    splitFiles.setBackground(new java.awt.Color(204, 204, 255));
    splitFiles.setOrientation(javax.swing.JSplitPane.VERTICAL_SPLIT);

    fileSelectionTable.setPreferredSize(new java.awt.Dimension(484, 80));
    splitFiles.setTopComponent(fileSelectionTable);

    recordPanel.setPreferredSize(new java.awt.Dimension(150, 37));
    recordPanel.setLayout(new java.awt.BorderLayout());

    transmitControlPanel.setBackground(new java.awt.Color(204, 255, 204));

    sendEcuapassButton.setBackground(new java.awt.Color(204, 237, 255));
    sendEcuapassButton.setText("<html>Transmitir al<br>ECUAPASS</html>");
    sendEcuapassButton.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(java.awt.event.ActionEvent evt) {
        sendEcuapassButtonActionPerformed(evt);
      }
    });
    transmitControlPanel.add(sendEcuapassButton);

    sendCodebinButton.setBackground(new java.awt.Color(255, 242, 153));
    sendCodebinButton.setText("<html>Transmitir al<br>CODEBIN</html>");
    sendCodebinButton.addActionListener(new java.awt.event.ActionListener() {
      public void actionPerformed(java.awt.event.ActionEvent evt) {
        sendCodebinButtonActionPerformed(evt);
      }
    });
    transmitControlPanel.add(sendCodebinButton);

    recordPanel.add(transmitControlPanel, java.awt.BorderLayout.SOUTH);
    recordPanel.add(ecuapassView, java.awt.BorderLayout.CENTER);

    splitFiles.setBottomComponent(recordPanel);

    splitImage.setRightComponent(splitFiles);

    imageView.setMinimumSize(new java.awt.Dimension(400, 500));
    splitImage.setLeftComponent(imageView);

    add(splitImage, java.awt.BorderLayout.CENTER);
  }// </editor-fold>//GEN-END:initComponents

  private void sendEcuapassButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_sendEcuapassButtonActionPerformed
    controller.onBotSubmitToEcuapass ();
  }//GEN-LAST:event_sendEcuapassButtonActionPerformed

  private void sendCodebinButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_sendCodebinButtonActionPerformed
    controller.onBotSubmitToCodebin ();
  }//GEN-LAST:event_sendCodebinButtonActionPerformed

  // Variables declaration - do not modify//GEN-BEGIN:variables
  private results.EcuapassView ecuapassView;
  private main.FileSelectionTable fileSelectionTable;
  private widgets.ImageViewLens imageView;
  private javax.swing.JPanel recordPanel;
  private javax.swing.JButton sendCodebinButton;
  private javax.swing.JButton sendEcuapassButton;
  private javax.swing.JSplitPane splitFiles;
  private javax.swing.JSplitPane splitImage;
  private javax.swing.JPanel transmitControlPanel;
  // End of variables declaration//GEN-END:variables

	Controller controller;

	public ResultsView () {
		initComponents ();
	}

	public void setController (Controller controller) {
		this.controller = controller;
		fileSelectionTable.setController (controller, "simpleTableProcessedFiles");
	}

	// 
	void setRecordView (EcuapassView recordView) {
		recordPanel.remove (this.ecuapassView);
		this.ecuapassView = recordView;
		this.ecuapassView.setController (controller);
		recordPanel.add (recordView, BorderLayout.CENTER);

		this.revalidate();
	}

	public void selectFirstRecord () {
		fileSelectionTable.selectFirstRow ();
	}

	// Getters
	public EcuapassView getFieldsView () {
		return ecuapassView;
	}
	
	public FileSelectionTable getFileSelectionTable () {
		return (fileSelectionTable);
	}

	public ImageViewLens getImageView () {
		return imageView;
	}
}
