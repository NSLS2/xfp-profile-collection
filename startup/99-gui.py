from matplotlib.backends.qt_compat import QtWidgets
import bluesky.plans as bp

class ColumnWidget:
    def __init__(self, layout, j):
        self._position = j
        cb = self.cb = QtWidgets.QGroupBox('Position {}'.format(j))
        cb.setCheckable(True)
        sb = self.sb = QtWidgets.QDoubleSpinBox()
        le = self.le = QtWidgets.QLineEdit('sample {}'.format(j))
        cb.toggled.connect(sb.setEnabled)
        cb.toggled.connect(le.setEnabled)
        cb.setChecked(True)

        f_layout = QtWidgets.QFormLayout()
        f_layout.addRow('name', le)
        f_layout.addRow('exposure[s]', sb)
        cb.setLayout(f_layout)

        layout.addWidget(cb)

    @property
    def enabled(self):
        return self.cb.isChecked()

    @property
    def name(self):
        return self.le.displayText()

    @property
    def position(self):
        return self._position

    @property
    def exposure(self):
        return self.sb.value()

class XFPSampleSelector:
    def __init__(self, num):
        self.window = window = QtWidgets.QMainWindow()
        window.setWindowTitle('XFP samples')
        mw = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()

        self.controls = tuple(ColumnWidget(layout, j) for j in range(num))

        mw.setLayout(layout)
        window.setCentralWidget(mw)

        window.show()

    def walk_values(self):
        return [{'name': d.name,
                 'exposure': d.exposure,
                 'position': d.position} for d in self.controls
                if d.enabled]

    def show(self):
        return self.window.show()

    @property
    def plan(self):
        for d in self.walk_values():
            yield from bp.mv(motor, d['position'])
            yield from bp.count([det, motor], md=d)

win = XFPSampleSelector(7)
win.show()
