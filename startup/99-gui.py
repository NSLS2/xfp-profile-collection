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
    def __init__(self):
        self.window = window = QtWidgets.QMainWindow()
        window.setWindowTitle('XFP samples')
        mw = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()

        self.controls = []
        
        for j in range(24):
            if j == 11:
                continue
            r, c = np.unravel_index(j, (4, 6))
            cw = ColumnWidget(j)
            layout.addWidget(cw.cb, r, c)
            self.controls.append(cw)

        mw.setLayout(layout)
        window.setCentralWidget(mw)

        self.rail_offset = -240
        self.rail_step = 15
        
        self.table_offset = 0.94974376 * np.ones(24)
        # self.table_offset = [...]

    def walk_values(self):
        return [{'exposure': d.exposure,
                 'position': d.position,
                 **d.md} for d in self.controls
                if d.enabled]

    def show(self):
        return self.window.show()

    def plan(self, file_name=None):
        uid_list = []
        for d in self.walk_values():
            yield from bp.abs_set(msh,
                                  (d['position'] * self.rail_step
                                   + self.rail_offset),
                                  group='msh')
            yield from bp.abs_set(tbl2,
                                  (self.table_offset[d['position']]),
                                  group='msh')
            yield from bp.wait('msh')

            # REPLACE THIS WITH GUTS THAT REALLY DO MEASUREMENT
            # uid = (yield from xfp_plan_fast_shutter(d['exposure'], md=d))
            uid = (yield from bp.count([msh, tbl2], md=d))
            
            if uid is not None:
                uid_list.append(uid)
                
        if uid_list:
            columns = ('uid', 'name', 'exposure', 'notes')
            tbl = pd.DataFrame([[h.start[c] for c in columns]
                                for h in db[uids]], columns=columns)
            self.last_table = tbl
            if file_name is not None:
                tbl.to_csv(file_name, index=False)

            
def xfp_plan(t):
    yield from bp.mv(delay_gen_time, t)
    yield from bp.mv(go_button, 1)
    return (yield from bp.count([msh, tbl2, delay_gen], md=d))

MSHgui = XFPSampleSelector()
MSHgui.show()
