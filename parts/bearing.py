"""
"""

import numpy as np
import matplotlib.pyplot as plt

class Bearing:
    def __init__(self, name, bore_diameter, outer_diameter, width,
                 load_center, contact_angle, factor, static_load_rating,
                 dynamic_load_rating, kxx, kyy, cxx, frequency=None):
        """
        Initialize bearing object from manufacturer data.
        """
        self.name = name
        self.d = bore_diameter
        self.D = outer_diameter
        self.B = width
        self.a = load_center
        self.alpha = contact_angle
        self.f0 = factor
        self.C0r = static_load_rating
        self.Cr = dynamic_load_rating
        self.kxx = kxx
        self.kyy = kyy
        self.cxx = cxx
        self.frequency = frequency

class BearingAdvanced:
    def __init__(self, name, bore_diameter, outer_diameter, width,
                 load_center, contact_angle, factor, static_load_rating,
                 dynamic_load_rating, equiv_dynamic_load_table, i = 1):
        """
        Initialize bearing object from manufacturer data.

        Format for dynamic load table is as follows:

                           | Fa/Fr < e | Fa/Fr > e |
        i*f0*Fa/C0r  |  e  |  X  |  Y  |  X  |  Y  |

        (n*6 array)
        """
        self.name = name
        self.d = bore_diameter
        self.D = outer_diameter
        self.B = width
        self.a = load_center
        self.alpha = contact_angle
        self.f0 = factor
        self.C0r = static_load_rating
        self.Cr = dynamic_load_rating
        self.table = equiv_dynamic_load_table
        self.i = i # 1 for single bearing, can be 2 for *some* dual
                   # bearing arrangements
        if self.table is not None:
            self.extrapolateTable()

    def extrapolateTable(self):
        """
        Extrapolates equivalent dynamic load table e, Y for zero axial force.
        """
        
        self.e_0 = self.table[0,1] + (self.table[0,1] - self.table[1,1])\
                *self.table[0,0]/(self.table[1,0]-self.table[0,0])

        self.Y_0 = self.table[0,5] + (self.table[0,5] - self.table[1,5])\
                *self.table[0,0]/(self.table[1,0]-self.table[0,0])
    
    def equivalentDynamicLoad(self, fa, fr, verbose=True):
        """
        Computes bearing equivalent dynamic load using linear interpolation
        of table data. "Extreme" values extrapolated as follows:

         - e and Y assumed constant past final value of i*f0*Fa/C0r

         - e and Y limit value for Fa = 0 obtained by linear extrapolation
        """

        criterion = self.i * self.f0 * fa / self.C0r

        e = np.interp(criterion,
                      [0] + list(self.table[:,0]),
                      [self.e_0] + list(self.table[:,1]))
         
        if verbose:
            print("###############################################")
            print("# Bearing Equivalent Dynamic Load Calculation #")
            print("#                                             #")
            print("# i*f0*Fa/C0r = {:.4f} --> e = {:.2f}           #"\
                    .format(criterion,e))
            print("#                                             #")
        
        if fa/fr <= e:
            X = np.interp(criterion, self.table[:,0], self.table[:,2])
            Y = np.interp(criterion, self.table[:,0], self.table[:,3])
            if verbose:
                print("# Fa/Fr = {:.2f} <= e --> X = {:.2f} and Y = {:.2f} #"\
                        .format(fa/fr, X, Y))
            self.comparison = "<"
        else:
            X = np.interp(criterion, self.table[:,0], self.table[:,4])
            Y = np.interp(criterion, [0]+list(self.table[:,0]),
                          [self.Y_0]+list(self.table[:,5]))
            if verbose:
                print("# Fa/Fr = {:.2f} > e --> X = {:.2f} and Y = {:.2f}  #"\
                        .format(fa/fr, X, Y))
            self.comparison = ">"
        if verbose:
            print("###############################################\n")

        self.criterion = criterion
        self.e = e
        self.X = X
        self.Y = Y

        return X*fr + Y*fa

    def draw(self):
        """
        Plots bearing "e" and "X,Y" versus axial load.
        """
        # e vs i*f0*Fa/C0r
        plt.figure(figsize=(4,3))

        plt.plot([0]+list(self.table[:,0])+[int(self.table[-1,0])+1],
                 [self.e_0]+list(self.table[:,1])+[self.table[-1,1]],
                 color = "k")
        plt.xlim(0, int(self.table[-1,0])+1)
        plt.ylim(0, 1)
        plt.xlabel(r"$i f_0 F_A/C_{0r}$")
        plt.ylabel(r"$e$")
        plt.locator_params(axis = "y", nbins = 5)

        figpath = "../../out/"+self.name+"_e.png"
        plt.savefig(figpath, dpi=300, bbox_inches="tight")

        # X,Y for Fa/Fr > e vs i*f0*Fa/C0r
        plt.figure(figsize=(4,3))
        
        plt.plot([0]+list(self.table[:,0])+[int(self.table[-1,0])+1],
                 [self.table[0,4]]+list(self.table[:,4])+[self.table[-1,4]],
                 color = "b", label = r"$X$ for $F_A/F_R > e$")
        plt.plot([0]+list(self.table[:,0])+[int(self.table[-1,0])+1],
                 [self.Y_0]+list(self.table[:,5])+[self.table[-1,5]],
                 color = "r", label = r"$Y$ for $F_A/F_R > e$")
        plt.legend()
        plt.xlim(0, int(self.table[-1,0])+1)
        plt.ylim(0, 2)
        plt.xlabel(r"$i f_0 F_A/C_{0r}$")
        plt.locator_params(axis = "y", nbins = 5)

        figpath = "../../out/"+self.name+"_xy.png" 
        plt.savefig(figpath, dpi=300, bbox_inches="tight")
