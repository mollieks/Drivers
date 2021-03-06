#!/usr/bin/env python3
import numpy as np
import logging
log = logging.getLogger('LabberDriver')


class Qubit:
    """Base class for different types of qubits."""

    def __init__(self):
        pass

    def f_to_V(self, f):
        """Convert qubit frequency to voltage.

        Parameters
        ----------
        f : float or list of floats
            Qubit frequencies.

        Returns
        -------
        float or list of floats
            Voltage corresponding to the frequencies.

        """
        pass

    def V_to_f(self, V):
        """Convert voltage to qubit frequency.

        Parameters
        ----------
        V : float or list of floats
            Bias voltage.

        Returns
        -------
        float or list of floats
            Qubit frequencies.

        """
        pass

    def df_to_dV(self, df):
        """Convert a change in qubit frequency to a change in voltage.

        Parameters
        ----------
        df : loat or list of floats
            Changes in qubit frequency.

        Returns
        -------
        float or list of floats
            Voltages corresponding to the change in frequency.

        """
        pass


class Transmon(Qubit):
    """Represent the transmon qubit.

    Parameters
    ----------
    f01_max : float
        Maximum qubit frequency.
    f01_min : float
        Mimimum qubit frequency. For symmetric transmons, put `f01_min` to 0.
    Ec : float
        Qubit Ec.
    Vperiod : float
        Voltage corresponding to 1 period.
    Voffset : float
        Offset voltage.
    V0 : float
        Operating point of the qubit.

    Attributes
    ----------
    EJS : float
        Sum of the Josephson energies.
    d : float
        Junction assymetry.

    """

    def __init__(self, f01_max, f01_min, Ec, Vperiod, Voffset, V0):
        self.f01_max = f01_max
        self.f01_min = f01_min
        self.Ec = Ec
        self.Vperiod = Vperiod
        self.Voffset = Voffset
        self.V0 = V0

        # Calculate the JJ parameters
        self.EJS = (self.f01_max + self.Ec)**2 / (8 * self.Ec)
        self.d = (self.f01_min + self.Ec)**2 / (8 * self.EJS * self.Ec)

    def V_to_f(self, V):  # noqa 102
        F = np.pi * (V + self.Voffset) / self.Vperiod
        f = np.sqrt(8 * self.EJS * self.Ec * np.abs(np.cos(F)) *
                    np.sqrt(1 + self.d**2 * np.tan(F)**2)) - self.Ec
        return f

    def f_to_V(self, f):  # noqa 102
        # fix types
        if type(f) is float:
            f = np.array([f])
        else:
            f = np.array(f)

        # Make sure frequencies are inside the possible frequency range
        if np.any(f > self.f01_max):
            raise ValueError(
                'Frequency requested is outside the qubit spectrum')
        if np.any(f < self.f01_min):
            raise ValueError(
                'Frequency requested is outside the qubit spectrum')

        # Calculate the required EJ for the given frequencies
        EJ = (f + self.Ec)**2 / (8 * self.Ec)

        # Calculate the F=pi*(V+voffset)/vperiod corresponding to that EJ
        sinF = np.sqrt((EJ**2 / self.EJS**2 - 1) / (self.d**2 - 1))
        # sinF is bounded from 0 to 1, and therefore F is bounded from 0 to
        # pi/2. This means that we're automatically staying on the first lobe
        # of the
        F = np.arcsin(sinF)

        # And finally the voltage
        V = F * self.Vperiod / np.pi - self.Voffset

        # Mirror around Voffset, bounding the qubit to one side of the maxima
        # if self.V0 >= self.Voffset:
        #     V[V < self.Voffset] = 2 * self.Voffset - V[V < self.Voffset]
        # else:
        #     V[V > self.Voffset] = 2 * self.Voffset - V[V > self.Voffset]
        # Stay within same half-period
        # Vmax = self.Vperiod / 2 + self.Voffset
        # Vmin = -self.Vperiod / 2 + self.Voffset
        # V[V > Vmax] = 2 * Vminp - V[V > Vminp]
        # V[V < Vmin] = 2 * Vminn - V[V < Vminn]
        return V

    def df_to_dV(self, df):  # noqa 102
        f0 = self.V_to_f(self.V0)
        return self.f_to_V(df + f0) - self.V0
