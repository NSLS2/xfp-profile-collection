from ophyd import (PseudoPositioner, PseudoSingle, EpicsMotor)
from ophyd import (Component as Cpt)
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)


class PseudoFilterWheel(PseudoPositioner):
    """Filter wheel pseudopositioner ophyd object."""

    # dict consists of the following fields:
    # position number: angle [degrees], thickness of material [um]
    wheel_positions = [{'name': 'Position 1', 'angle': 0., 'thickness': 0},
                       {'name': 'Position 2', 'angle': 45., 'thickness': 762},
                       {'name': 'Position 3', 'angle': 90., 'thickness': 508},
                       {'name': 'Position 4', 'angle': 135., 'thickness': 305},
                       {'name': 'Position 5', 'angle': 180., 'thickness': 203},
                       {'name': 'Position 6', 'angle': 225., 'thickness': 152},
                       {'name': 'Position 7', 'angle': 270., 'thickness': 76},
                       {'name': 'Position 8', 'angle': 315., 'thickness': 25}]

    _tolerance = 1e-2
    _thickness_egu = 'um'
    _thicknesses = tuple([v['thickness'] for v in wheel_positions])
    _angles = tuple([v['angle'] for v in wheel_positions])

    # Pseudo positioner: thickness
    thickness = Cpt(PseudoSingle, limits=(min(_thicknesses), max(_thicknesses)), egu=_thickness_egu)

    # Real positioner: angle
    angle = Cpt(EpicsMotor, 'XF:17BMA-ES:1{Fltr:1-Ax:Rot}Mtr')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        time.sleep(1)
        self._angle_egu = self.angle.egu

        # Update the wheel_positions list of dicts with the units:
        for i, _ in enumerate(self.wheel_positions):
            self.wheel_positions[i].update(angle_egu=self._angle_egu,
                                           thickness_egu=self._thickness_egu)

    @pseudo_position_argument
    def forward(self, pseudo_pos):
        '''Run a forward (pseudo -> real) calculation'''
        angle_val = None
        for pos in self.wheel_positions:
            if abs(pos['thickness'] - getattr(pseudo_pos, 'thickness')) < self._tolerance:
                angle_val = pos['angle']
        if angle_val is None and not self.angle._moving:
            # We throw the exception if the motor is not moving,
            # otherwise we get a lot of errors as an unexpected
            # `None` value is passed back.
            raise ValueError(f'Angle value cannot be found for '
                             f'the specified thickness {pseudo_pos.thickness}.\n'
                             f'Available thickness values are: {self._thicknesses}')
        elif self.angle._moving:
            # TODO: do it a better/smart way
            return self.RealPosition(angle=-1)
        else:
            return self.RealPosition(angle=angle_val)

    @real_position_argument
    def inverse(self, real_pos):
        '''Run an inverse (real -> pseudo) calculation'''
        thickness_val = None
        for pos in self.wheel_positions:
            if abs(pos['angle'] - getattr(real_pos, 'angle')) < self._tolerance:
                thickness_val = pos['thickness']
        if thickness_val is None and not self.angle._moving:
            # We throw the exception if the motor is not moving,
            # otherwise we get a lot of errors as an unexpected
            # `None` value is passed back.
            raise ValueError(f'Thickness value cannot be found for '
                             f'the specified angle {real_pos.angle}.\n'
                             f'Available angle values are: {self._angles}')
        elif self.angle._moving:
            # TODO: do it a better/smart way
            return self.PseudoPosition(thickness=-1)
        else:
            return self.PseudoPosition(thickness=thickness_val)


filter_wheel = PseudoFilterWheel(name='filter_wheel')
