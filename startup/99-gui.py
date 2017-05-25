from matplotlib.backends.qt_compat import QtWidgets
import bluesky.plans as bp
import pandas as pd

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

class XFPSampleSelector:
    def __init__(self, h_pos, v_pos):
        self.window = window = QtWidgets.QMainWindow()
        window.setWindowTitle('XFP Mult-Sample Holder Samples')
        mw = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()

        self.controls = []
        
        for j in range(24):
            if j == 10:
                continue
            r, c = np.unravel_index(j, (4, 6))
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
        uid_list = []
        for d in self.walk_values():
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
    
    return (yield from bp.count([msh, mshlift, pin_diode
                                ], md=d))

v_pos = np.array(
       [-.31, -0.33, -0.29, -0.28, -0.21696265,
       -0.24448264, -0.10, -0.26 , -0.22486145, -0.19,
               np.nan, -0.24427941, -0.14578496, -0.20066818, -0.21102896,
       -0.04099325, -0.08536624, -0.12224383, -0.10009569, -0.10,
       -0.14782382, -0.18598082, -0.10, -0.06438867])

h_pos = np.array(
      [-210.22962677, -195.17671138, -180.24262494, -165.120419  ,
       -150.23601044, -135.4387167 , -120.41666077, -105.55154939,
        -90.49264254,  -75.23829315,  -60.45       ,  -45.0,
        -29.8,  -14.91672256,    0.3,   15.5016519,
         30.55801061,   45.26752689,   60.38711324,   75.35637427,
         90.49112622,  105.31326202,  120.36494778,  135.36070856])
 
try:
    MSHgui.close()
except NameError:
    pass
MSHgui = XFPSampleSelector(h_pos, v_pos)
MSHgui.uncheck()
#MSHgui.show()


#Need to add in an obvious go button to gui
#Good to have a pause/unpause (with shutter closings as fail-safe)
