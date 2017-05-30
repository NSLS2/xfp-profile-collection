from matplotlib.backends.qt_compat import QtWidgets, QtCore, QtGui
from databroker_browser.qt import BrowserWindow, CrossSection, StackViewer
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
            raise Exception("path does not exst")

    @QtCore.Slot()
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
        
        
class XFPSampleSelector:
    def __init__(self, h_pos, v_pos):
        self.window = window = QtWidgets.QMainWindow()
        window.setWindowTitle('XFP Mult-Sample Holder Samples')
        mw = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        self.path_select = path = DirectorySelector('CSV path')
        self.controls = []
        
        for j in range(24):
            r, c = np.unravel_index(j, (4, 6))            
            if j == 10:
                layout.addWidget(path.widget, r, c)
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

    def uncheck(self):
        MSHgui.controls
        for column in MSHgui.controls:                                          
            column.cb.setChecked(False)
        for column in MSHgui.controls:
            column.cb.setChecked(False)

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
       [.3, 0.3, 0.4, .6, 0.3,
       0.4, 0.30, 0.25 , 0.4, 0.4,
               np.nan, 0.5, .35, 0.45, 0.35,
       0.4, 0.7, 0.6, 0.6, 0.65,
       0.65, 0.75, 0.75, 0.9])

h_pos = np.array(
      [-210.3, -195.2, -180.3, -165.1  ,
       -150.3, -135.53 , -120.51, -105.65,
        -90.59,  -75.34,  -60.55,  -45.1,
        -29.9,  -15,    0.2,   15.4,
         30.5,   45.5,   60.28,   75.25,
         90.39,  105.21,  120.26,  135.26])
 
try:
    MSHgui.close()
except NameError:
    pass
MSHgui = XFPSampleSelector(h_pos, v_pos)
#MSHgui.show()


#Need to add in an obvious go button to gui
#Good to have a pause/unpause (with shutter closings as fail-safe)




search_result = lambda h: "{start[plan_name]} ['{start[uid]:.6}']".format(**h)
text_summary = lambda h: "This is a {start[plan_name]}.".format(**h)


def fig_dispatch(header, factory):
    plan_name = header['start']['plan_name']
    if 'image_det' in header['start']['detectors']:
        fig = factory('Image Series')
        cs = CrossSection(fig)
        sv = StackViewer(cs, db.get_images(header, 'image'))
    elif len(header['start'].get('motors', [])) == 1:
        motor, = header['start']['motors']
        main_det, *_ = header['start']['detectors']
        fig = factory("{} vs {}".format(main_det, motor))
        ax = fig.gca()
        lp = LivePlot(main_det, motor, ax=ax)
        db.process(header, lp)


def browse():
    return BrowserWindow(db, fig_dispatch, text_summary, search_result)
