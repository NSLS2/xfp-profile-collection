import numpy as np

#TODO(mr): remove later, for dev/tests only:
import matplotlib.pyplot as plt
plt.ion()
from bluesky.utils import install_qt_kicker
install_qt_kicker()

from matplotlib.backends.qt_compat import QtWidgets, QtCore, QtGui


import bluesky.plans as bp
import pandas as pd
import os

class ColumnWidget:
    def __init__(self, j):
        self._position = j
        cb = self.cb = QtWidgets.QGroupBox('Position {}'.format(j))
        cb.setCheckable(True)
        sb = self.sb = QtWidgets.QDoubleSpinBox()
        sb.setValue(10)
        sb.setMinimum(10)
        sb.setMaximum(20000)
        le = self.le = QtWidgets.QLineEdit('sample {}'.format(j))
        notes = self.notes = QtWidgets.QTextEdit(''.format(j))
        cb.toggled.connect(sb.setEnabled)
        cb.toggled.connect(le.setEnabled)
        cb.setChecked(True)

        f_layout = QtWidgets.QFormLayout()
        f_layout.addRow('name', le)
        f_layout.addRow('exposure[ms]', sb)
        f_layout.addRow('notes', notes)
              
        cb.setLayout(f_layout)

    @property
    def enabled(self):
        return self.cb.isChecked()

    @property
    def md(self):
        return {'name': self.le.displayText(),
                'notes': self.notes.toPlainText()}

    @property
    def position(self):
        return self._position

    @property
    def exposure(self):
        return self.sb.value()
    
class DirectorySelector:
    '''
    A widget class deal with selecting and displaying path names
    '''

    def __init__(self, caption, path=''):
        self.cap = caption
        widget = self.widget = QtWidgets.QGroupBox(caption)
        notes = self.notes = QtWidgets.QTextEdit('')

        hlayout = QtWidgets.QHBoxLayout()
        self.label = label = QtWidgets.QLabel(path)
        short_desc = self.short_desc = QtWidgets.QLineEdit('')
            
        hlayout.addWidget(self.label)
        hlayout.addStretch()
        button = QtWidgets.QPushButton('')
        button.setIcon(QtGui.QIcon.fromTheme('folder'))
        button.clicked.connect(self.select_path)
        # hlayout.addWidget(button)
        
        f_layout = QtWidgets.QFormLayout()
        f_layout.addRow(button, hlayout)
        f_layout.addRow('short description', short_desc)
        # f_layout.addRow('overall notes', notes)
              
        widget.setLayout(f_layout)

    @QtCore.Slot(str)
    def set_path(self, path):
        if os.path.isdir(path):
            self.label.setText(path)
        else:
            raise Exception("path does not exist")

    # @QtCore.Slot()
    def select_path(self):
        cur_path = self.path
        if len(cur_path) == 0:
            cur_path = ''
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self.widget, caption=self.cap, directory=cur_path)

        if len(path) > 0:
            self.path = path
            return path
        else:
            path = None
        return path

    @property
    def path(self):
        return self.label.text()

    @path.setter
    def path(self, in_path):
        self.set_path(in_path)

class RunEngineControls:
    def __init__(self, RE, GUI):
        self.RE = RE
        self.GUI = GUI

        self.widget = button_widget = QtWidgets.QWidget() 
        button_layout = QtWidgets.QHBoxLayout()
        button_widget.setLayout(button_layout)

        label = QtWidgets.QLabel('Idle')
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet('QLabel {background-color: green; color: white}')
        button_layout.addWidget(label)

        # Run button to execute RE
        button_run = QtWidgets.QPushButton('Run')
        button_run.clicked.connect(self.run)
        button_layout.addWidget(button_run)

        # Run button to execute RE
        button_pause = QtWidgets.QPushButton('Pause')
        button_pause.clicked.connect(self.pause)
        button_layout.addWidget(button_pause)

        self.label = label
        self.button_run = button_run
        self.button_pause = button_pause
        self.RE.state_hook = self.handle_state_change
        self.handle_state_change(self.RE.state, None)

    def run(self):
        if self.RE.state == 'idle':
            self.RE(self.GUI.plan())
        else:
            self.RE.resume()

    def pause(self):
        if self.RE.state == 'running':
            self.RE.request_pause()
        elif self.RE.state == 'paused':
            self.RE.stop()

    def handle_state_change(self, new, old):
        if new == 'idle':
            state = 'Idle'
            color = 'green'
            button_run_enabled = True
            button_pause_enabled = False
            button_run_text = 'Run'
            button_pause_text = 'Pause'
        elif new == 'paused':
            state = 'Paused'
            color = 'blue'
            button_run_enabled = True
            button_pause_enabled = True
            button_run_text = 'Resume'
            button_pause_text = 'Stop'
        elif new == 'running':
            state = 'Running'
            color = 'red'
            button_run_enabled = False
            button_pause_enabled = True
            button_run_text = 'Run'
            button_pause_text = 'Pause'

        self.label.setStyleSheet(f'QLabel {{background-color: {color}; color: white}}')
        self.label.setText(state)

        self.button_run.setEnabled(button_run_enabled)
        self.button_run.setText(button_run_text)
        self.button_pause.setEnabled(button_pause_enabled)
        self.button_pause.setText(button_pause_text)

        
class XFPSampleSelector:
    def __init__(self, h_pos, v_pos, rows=4, cols=6):
        self.window = window = QtWidgets.QMainWindow()
        window.setWindowTitle('XFP Multi-Sample Holder')
        mw = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()

        self.path_select = path = DirectorySelector('CSV path')
        self.controls = []
        self.re_controls = RunEngineControls(RE, self)

        for j in range(rows*cols):
            r, c = np.unravel_index(j, (rows, cols))
            if j == 10:

                w = QtWidgets.QWidget()
                wbox = QtWidgets.QVBoxLayout()
                w.setLayout(wbox)
                layout.addWidget(w, r, c)

                wbox.addWidget(path.widget)
                wbox.addWidget(self.re_controls.widget)

                button_toggle_all = QtWidgets.QPushButton('Check/Uncheck')
                button_toggle_all.setCheckable(True)
                button_toggle_all.setChecked(True)
                button_toggle_all.toggled.connect(self.toggle_all)
                wbox.addWidget(button_toggle_all)

                continue

            cw = ColumnWidget(j)
            layout.addWidget(cw.cb, r, c)
            self.controls.append(cw)

        mw.setLayout(layout)
        window.setCentralWidget(mw)

        self.h_pos = h_pos
        self.v_pos = v_pos


    def walk_values(self):
        return [{'exposure': d.exposure,
                 'position': d.position,
                 **d.md} for d in self.controls
                if d.enabled]

    def show(self):
        return self.window.show()

    def close(self):
        return self.window.close()

    def toggle_all(self, state):
        for column in self.controls:
            column.cb.setChecked(state)

    def plan(self, file_name=None):
        reason = self.path_select.short_desc.displayText()
        run_notes = self.path_select.notes.toPlainText()
        if file_name is None:
            gui_path = self.path_select.path
            if gui_path and reason:
                fname = '_'.join(reason.split()) + '.csv'
                file_name = os.path.join(gui_path, fname)
        print(file_name)

        uid_list = []
        base_md = {'plan_name': 'msh'}
        if reason:
            base_md['reason'] = reason
            
        for gui_d in self.walk_values():
            d = dict(base_md)
            d.update(gui_d)
            
            yield from bp.abs_set(msh,
                                  self.h_pos[d['position']],
                                  group='msh')
            yield from bp.abs_set(mshlift,
                                  self.v_pos[d['position']],
                                  group='msh')
            # awlays want to wait at least 3 seconds
            yield from bp.sleep(3)	    
            yield from bp.wait('msh')
  
            uid = (yield from xfp_plan_fast_shutter(d))
            #uid = (yield from bp.count([msh, mshlift], md=d))
            
            if uid is not None:
                uid_list.append(uid)
                
        if uid_list:
            columns = ('uid', 'name', 'exposure', 'notes')
            tbl = pd.DataFrame([[h.start[c] for c in columns]
                                for h in db[uid_list]], columns=columns)
            self.last_table = tbl
            if file_name is not None:
                tbl.to_csv(file_name, index=False)

        yield from bp.mv(msh, -275)
            
def xfp_plan_fast_shutter(d):
    exp_time = d['exposure']/1000

    yield from bp.mv(dg, exp_time)
    #open the protective shutter
    yield from bp.abs_set(shutter, 'Open', wait=True)
  
    #fire the fast shutter and wait for it to close again

    yield from bp.mv(dg.fire, 1)
    yield from bp.sleep(exp_time*1.1)

    #close the protective shutter
    yield from bp.abs_set(shutter, 'Close', wait=True)
    
    return (yield from bp.count([msh, mshlift, # pin_diode
                                ], md=d))

v_pos = np.array(
       [ 8.6,  8.6,  8.6,  8.6,  8.6,
        8.6,  8.6,  8.6,  8.6 ,  8.6,
               np.nan,  8.6,  8.6,  8.6,  8.6,
        8.6,  8.6,  8.6,  8.6,  8.6,
        8.6,  8.6,  8.6,  8.6 ])

h_pos = np.array(
      [-210.1,  -194.84,  -179.9,
        -165.09,  -150.41,  -135.41,
        -120.49,  -105.62,  -90.56,
        -75.21,  -60.62,  -44.87,
        -29.67,  -15,   0.14,
         15.24,   30.49,   45.2,
         60.22,   75.4,   90.1,
         105.4,   120.59,   135.49])
 
try:
    MSHgui.close()
except NameError:
    pass
MSHgui = XFPSampleSelector(h_pos, v_pos)
# MSHgui.show()


#Need to add in an obvious go button to gui
#Good to have a pause/unpause (with shutter closings as fail-safe)

#TODO(mr): move to a separate file:
# from databroker_browser.qt import BrowserWindow, CrossSection, StackViewer

#TODO(mrakitin): move the code below to a separate module - the code is unrelated:
# search_result = lambda h: "{start[plan_name]} ['{start[uid]:.6}']".format(**h)
# text_summary = lambda h: "This is a {start[plan_name]}.".format(**h)

# def fig_dispatch(header, factory):
#     plan_name = header['start']['plan_name']
#     if 'image_det' in header['start']['detectors']:
#         fig = factory('Image Series')
#         cs = CrossSection(fig)
#         sv = StackViewer(cs, db.get_images(header, 'image'))
#     elif len(header['start'].get('motors', [])) == 1:
#         motor, = header['start']['motors']
#         main_det, *_ = header['start']['detectors']
#         fig = factory("{} vs {}".format(main_det, motor))
#         ax = fig.gca()
#         lp = LivePlot(main_det, motor, ax=ax)
#         db.process(header, lp)
#
#
# def browse():
#     return BrowserWindow(db, fig_dispatch, text_summary, search_result)
