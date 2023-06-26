#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Equalizer
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class equalizer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Equalizer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Equalizer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "equalizer")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.Trebel = Trebel = 0.5
        self.Mid = Mid = 0.5
        self.KILO = KILO = 1e3
        self.Base = Base = 0.5

        ##################################################
        # Blocks
        ##################################################

        self._Trebel_range = Range(0, 1, 0.1, 0.5, 1)
        self._Trebel_win = RangeWidget(self._Trebel_range, self.set_Trebel, "'Trebel'", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Trebel_win)
        self._Mid_range = Range(0, 1, 0.1, 0.5, 1)
        self._Mid_win = RangeWidget(self._Mid_range, self.set_Mid, "'Mid'", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Mid_win)
        self._Base_range = Range(0, 1, 0.1, 0.5, 1)
        self._Base_win = RangeWidget(self._Base_range, self.set_Base, "'Base'", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Base_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_f(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["dark red", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\senti\\Desktop\\github\\GNU_Radio\\Book I - Fieldxp - Intro to SDR\\07 Equalizer\\HumanEvents_s32k.wav', True)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.band_pass_filter_0_1 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                Trebel,
                samp_rate,
                (2.6*KILO),
                (10*KILO),
                10,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                Mid,
                samp_rate,
                400,
                (2.6*KILO),
                10,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                Base,
                samp_rate,
                20,
                400,
                10,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_0 = audio.sink(samp_rate, '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.band_pass_filter_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.band_pass_filter_0_1, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_add_xx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.band_pass_filter_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "equalizer")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.band_pass(self.Base, self.samp_rate, 20, 400, 10, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(self.Mid, self.samp_rate, 400, (2.6*self.KILO), 10, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.band_pass(self.Trebel, self.samp_rate, (2.6*self.KILO), (10*self.KILO), 10, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_Trebel(self):
        return self.Trebel

    def set_Trebel(self, Trebel):
        self.Trebel = Trebel
        self.band_pass_filter_0_1.set_taps(firdes.band_pass(self.Trebel, self.samp_rate, (2.6*self.KILO), (10*self.KILO), 10, window.WIN_HAMMING, 6.76))

    def get_Mid(self):
        return self.Mid

    def set_Mid(self, Mid):
        self.Mid = Mid
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(self.Mid, self.samp_rate, 400, (2.6*self.KILO), 10, window.WIN_HAMMING, 6.76))

    def get_KILO(self):
        return self.KILO

    def set_KILO(self, KILO):
        self.KILO = KILO
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(self.Mid, self.samp_rate, 400, (2.6*self.KILO), 10, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.band_pass(self.Trebel, self.samp_rate, (2.6*self.KILO), (10*self.KILO), 10, window.WIN_HAMMING, 6.76))

    def get_Base(self):
        return self.Base

    def set_Base(self, Base):
        self.Base = Base
        self.band_pass_filter_0.set_taps(firdes.band_pass(self.Base, self.samp_rate, 20, 400, 10, window.WIN_HAMMING, 6.76))




def main(top_block_cls=equalizer, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
