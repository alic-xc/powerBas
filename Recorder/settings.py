from decouple import config
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QGridLayout,
                             QLabel, QComboBox, QGroupBox, QVBoxLayout, QFormLayout, QRadioButton, QHBoxLayout,
                             QFileDialog, QPushButton, QCheckBox, QLayout, QMessageBox)
from Sounder.device_lists import SounderDevices
from db import DBWrapper
import os
import sys


class SettingsDialog(QDialog):
    """
    Dialog window for configuring powerbas recording software.
    """

    def __init__(self, parent=None):
        """ Initialize the dialog window with all the component required. """

        super().__init__(parent)
        self.setWindowTitle("Powerbas settings")
        self.setGeometry(100, 100, 500, 400)  # Set application width and height

        layout = self._settings_layout()
        self.setStyleSheet("font-size:13px")

        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)
        self._system_settings(layout)
        self._save_settings(layout)

        # Initialize a connection to the database
        try:
            self.db = DBWrapper()
        except Exception as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Message Panel")
            msg.setInformativeText("An error has occured")
            msg.setWindowTitle("MessageBox demo")
            msg.setDetailedText("The details are as follows:\n" + str(error))
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.buttonClicked.connect(self.exit)
            msg.exec_()

        finally:
            pass
            # if self.connection is not None:
            #     self.connection.close()

    def exit(self):
        """ Exit application. """
        return sys.exit(0)

    def save(self, *args, **kwargs):
        """ Signal for saving data to the database. """

    def _settings_layout(self):
        """ Set the base layout """
        layout = QGridLayout()
        return layout

    def _save_settings(self, layout):
        """ UI for saving and exiting the application."""
        self.actionButton = QDialogButtonBox()
        self.actionButton.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.actionButton.accepted.connect(self.save)
        self.actionButton.rejected.connect(self.exit)
        layout.addWidget(self.actionButton)

    def _system_settings(self, layout):
        """ GUI for sampling rate and logic """
        groupbox = QGroupBox("System Settings")
        layout.addWidget(groupbox, 0,0)
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        groupbox.setLayout(form_layout)
        # Draw UI
        self.sampling(form_layout)
        self.bitrate(form_layout)
        self.devices(form_layout)
        self.channels(form_layout)
        self.destination(form_layout)
        self.duration(form_layout)
        self.automate_recording(form_layout)
        self.am_checkboxes(form_layout)
        self.pm_checkboxes(form_layout)


    def sampling(self, form_layout):
        """ """
        self.sampling = QComboBox(self)
        self.sampling_list = {
            '44,100khz (Highly Recommended)': 44100,
            '48,00khz': 48000,
            '20,00khz (Use with caution)': 20000
        }
        self.sampling.addItems(self.sampling_list)
        form_layout.addRow('Sampling Rate: ', self.sampling)

    def bitrate(self, form_layout):
        """ Bit rate UI """
        self.bitrates = QComboBox(self)
        self.bitrate_list = {
            'Int24 (Highly Recommend)': 24,
            'Int8': 8,
            'Int16': 16,
            'Int32': 32,
            'Float32': 64,
        }
        self.bitrates.addItems(self.bitrate_list)
        form_layout.addRow('Bit Rate: ', self.bitrates)

    def devices(self, form_layout):
        """ Devices UI """
        self.devices = QComboBox(self)
        devices = SounderDevices()
        avail_devices = devices.getdevices()['0']
        self.device_list = {}
        self.device_list.update(avail_devices)
        self.devices.addItems(self.device_list)
        form_layout.addRow('Recording Device: ', self.devices)

    def channels(self, form_layout):
        """ Audio channel UI"""
        self.channel = QComboBox(self)
        self.channel_list = {
            'mono (1)': 1,
            'stero (2)': 2
        }
        self.channel.addItems(self.channel_list)
        form_layout.addRow('Audio Channel: ', self.channel)
        form_layout.setAlignment(QtCore.Qt.AlignLeft)

    def destination(self, form_layout):
        """ Recording destination """
        self.button = QPushButton("Choose Dir")
        self.display_dir = QLabel("Not Set")
        self.button.clicked.connect(self.set_directory)
        self.button.setFixedWidth(100)
        form_layout.addRow(self.button, self.display_dir)

    def duration(self, form_layout):
        """ Audio recording duration UI """
        self.duration = QComboBox()
        self.durations = {
            '3m': 180,
            '6m': 360,
            '10m': 600,
        }
        self.duration.addItems(self.durations)
        self.duration.setFixedWidth(250)
        form_layout.addRow('Duration', self.duration)

    def automate_recording(self, form_layout):
        """ Automate recording UI"""
        auto_label = QLabel('Auto Recording')
        form_layout.addRow(auto_label)

        # Automatic Recording
        self.auto_radio = QRadioButton("Yes")
        self.auto_radio.setChecked(True)
        self.auto_radio.recording = "yes"
        self.auto_radio.toggled.connect(self.hideAvailTime)
        form_layout.addRow(self.auto_radio)

        # Manual Recording
        self.manual_radio = QRadioButton("No")
        self.manual_radio.recording = "no"
        self.manual_radio.toggled.connect(self.displayAvailTime)
        form_layout.addRow(self.manual_radio)

    def am_checkboxes(self, form_layout):
        """ Checkboxes for managing AM time for manual recording """
        self.groupTimebox = QGroupBox("AM")
        self.groupTimebox.hide()
        form_layout.addRow(self.groupTimebox)
        time_layout = QGridLayout()
        self.groupTimebox.setLayout(time_layout)

        am_12 = QCheckBox("12:00 AM")
        am_12.value = 0
        time_layout.addWidget(am_12, 0, 0)

        am_1 = QCheckBox("1:00 AM")
        am_1.value = 1
        time_layout.addWidget(am_1, 0, 1)

        am_2 = QCheckBox("2:00 AM")
        am_2.value = 2
        time_layout.addWidget(self.am_2, 0, 2)

        am_3 = QCheckBox("3:00 AM")
        am_3.value = 3
        time_layout.addWidget(am_3, 0, 3)

        am_4 = QCheckBox("4:00 AM")
        am_4.value = 4
        time_layout.addWidget(am_4, 1, 0)

        am_5 = QCheckBox("5:00 AM")
        am_5.value = 5
        time_layout.addWidget(am_5, 1, 1)

        am_6 = QCheckBox("6:00 AM")
        am_6.value = 6
        time_layout.addWidget(am_6, 1, 2)

        am_7 = QCheckBox("7:00 AM")
        am_7.value = 7
        time_layout.addWidget(am_7, 1, 3)

        am_8 = QCheckBox("8:00 AM")
        am_8.value = 8
        time_layout.addWidget(am_8, 2, 0)

        am_9 = QCheckBox("9:00 AM")
        am_9.value = 9
        time_layout.addWidget(am_9, 2, 1)

        am_10 = QCheckBox("10:00 AM")
        am_10.value = 10
        time_layout.addWidget(am_10, 2, 2)

        am_11 = QCheckBox("11:00 AM")
        am_11.value = 11
        time_layout.addWidget(am_11, 2, 3)

    def pm_checkboxes(self, form_layout ):
        """ Checkboxes for managing PM time for manual recording """
        self.groupTimePMbox = QGroupBox("PM")
        self.groupTimePMbox.hide()
        form_layout.addRow(self.groupTimePMbox)
        pm_time_layout = QGridLayout()
        self.groupTimePMbox.setLayout(pm_time_layout)
        pm_12 = QCheckBox("12:00 PM")
        pm_12.value = 12
        pm_time_layout.addWidget(pm_12, 0, 0)

        pm_1 = QCheckBox("1:00 PM")
        pm_12.value = 13
        pm_time_layout.addWidget(pm_1, 0, 1)

        pm_2 = QCheckBox("2:00 PM")
        pm_2.value = 14
        pm_time_layout.addWidget(pm_2, 0, 2)

        pm_3 = QCheckBox("3:00 PM")
        pm_3.value = 15
        pm_time_layout.addWidget(pm_3, 0, 3)

        pm_4 = QCheckBox("4:00 PM")
        pm_4.value = 16
        pm_time_layout.addWidget(pm_4, 1, 0)

        pm_5 = QCheckBox("5:00 PM")
        pm_5.value = 17
        pm_time_layout.addWidget(pm_5, 1, 1)

        pm_6 = QCheckBox("6:00 PM")
        pm_6.value = 18
        pm_time_layout.addWidget(pm_6, 1, 2)

        pm_7 = QCheckBox("7:00 PM")
        pm_7.value = 19
        pm_time_layout.addWidget(pm_7, 1, 3)

        pm_8 = QCheckBox("8:00 PM")
        pm_8.value = 20
        pm_time_layout.addWidget(pm_8, 2, 0)

        pm_9 = QCheckBox("9:00 PM")
        pm_9.value = 21
        pm_time_layout.addWidget(pm_9, 2, 1)

        pm_10 = QCheckBox("10:00 PM")
        pm_10.value = 22
        pm_time_layout.addWidget(pm_10, 2, 2)

        pm_11 = QCheckBox("11:00 PM")
        pm_11.value = 23
        pm_time_layout.addWidget(pm_11, 2, 3)

    def load_saved_data(self):
        """ Preload data """
        pass


    def save_data(self):
        """ Get all saved data """
        device = self.device_list.get(self.devices.currentText())
        sampling_rate = self.sampling_list.get(self.sampling.currentText())
        bit_rate = self.bitrate_list.get(self.bitrates.currentText())
        channel = self.channel_list.get(self.channel.currentText())
        directory = self.display_dir.text()
        duration = self.durations.get(self.duration.currentText())
        automate_recording = True if self.auto_radio.isChecked() else False
        passed = True
        msg = []

        if device is None:
            msg.append("Device not recognised")
            passed = False

        if sampling_rate is None:
            msg.append("Sampling rate not recognised")
            passed = False

        if bit_rate is None:
            msg.append("Bit rate not recognised")
            passed = False

        if channel is None:
            msg.append("Channel not recognised")
            passed = False

        if not os.path.isdir(directory):
            msg.append("Recording destination not exist/recognised")
            passed = False

        if duration is None:
            msg.append("Duration not recognised")
            passed = False

        if automate_recording == True:
            print()


        if not passed:
            self.display_msg(msg, 'warning', proceed=True)
        else:
            data = {
                'device': device,
                'sampling_rate': sampling_rate,
                'bit_rate': bit_rate,
                'channel': channel,
                'destination': directory,
                'duration': duration,
                'automatic_recording': automate_recording,
                # 'recording_time': setting_obj.recording_time
            }
            print(data)


    def display_msg(self, error, type, proceed=False, autostart=True):
        msg = QMessageBox()

        if type == 'critical':
            msg.setIcon(QMessageBox.Critical)
        elif type == 'warning':
            msg.setIcon(QMessageBox.Warning)
        else:
            msg.setIcon(QMessageBox.Information)

        msg.setText("Message Panel")
        msg.setInformativeText("An error has occured!")
        msg.setWindowTitle("Unable to progress")
        msg.setDetailedText("The details are as follows:\n" + str(error))
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        if not proceed:
            msg.buttonClicked.connect(self.exit)

        msg.exec_()

    def displayAvailTime(self):
        """ """
        self.save_data()
        self.groupTimebox.show()
        self.groupTimePMbox.show()
        self.resize(500, 400)  # Set application width and height

    def hideAvailTime(self):
        """ Hide the list of time when the auto recording is active. Also resize the window """
        self.groupTimebox.hide()
        self.groupTimePMbox.hide()
        self.resize(500, 400)  # Set application width and height

    def set_directory(self, *args, **kwargs):
        """ Select or change the recording destination. """
        select_directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.display_dir.setText(select_directory)
        print(select_directory)


if __name__ == '__main__':
    # Execute code
    app = QApplication(sys.argv)
    settingsDialog = SettingsDialog()
    settingsDialog.show()
    sys.exit(app.exec_())

