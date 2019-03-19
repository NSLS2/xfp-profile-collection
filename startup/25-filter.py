from ophyd import (PseudoPositioner, PseudoSingle, EpicsMotor)
from ophyd import (Component as Cpt)
from ophyd.pseudopos import (pseudo_position_argument,
                             real_position_argument)


class PseudoFilterWheel(PseudoPositioner):
    """Filter wheel pseudopositioner ophyd object."""

    # dict consists of the following fields:
    # position number: angle [degrees], thickness of material [um]
    wheel_positions = {1: {'angle': 0, 'thickness': 0},
                       2: {'angle': 45, 'thickness': 762},
                       3: {'angle': 90, 'thickness': 508},
                       4: {'angle': 135, 'thickness': 305},
                       5: {'angle': 180, 'thickness': 203},
                       6: {'angle': 225, 'thickness': 152},
                       7: {'angle': 270, 'thickness': 76},
                       8: {'angle': 315, 'thickness': 25}}

    _thicknesses = tuple([v['thickness'] for k, v in wheel_positions.items()])
    _angles = tuple([v['angle'] for k, v in wheel_positions.items()])

    # Pseudo positioner: thickness
    thickness = Cpt(PseudoSingle, limits=(min(_thicknesses), max(_thicknesses)), egu='um')

    # Real positioner: angle
    angle = Cpt(EpicsMotor, 'XF:17BMA-ES:1{Fltr:1-Ax:Rot}Mtr')

    @pseudo_position_argument
    def forward(self, pseudo_pos, tol=1e-2):
        '''Run a forward (pseudo -> real) calculation'''
        angle_val = None
        for k, v in self.wheel_positions.items():
            if abs(v['thickness'] - getattr(pseudo_pos, 'thickness')) < tol:
                angle_val = v['angle']
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
    def inverse(self, real_pos, tol=1e-2):
        '''Run an inverse (real -> pseudo) calculation'''
        thickness_val = None
        for k, v in self.wheel_positions.items():
            if abs(v['angle'] - getattr(real_pos, 'angle')) < tol:
                thickness_val = v['thickness']
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
