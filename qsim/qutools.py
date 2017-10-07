import qutip as qt
from pylab import *
import matplotlib.colors as clr

def plot_wigner(rho, ax=None, cmap="RdBu", cbar=False):
    if ax == None: f,ax = subplots()
    xvec = linspace(-sqrt(rho.dims[0][0]), sqrt(rho.dims[0][0]), 100)
    wigner_mat = qt.wigner(rho,xvec,xvec)
    vmax = wigner_mat.max()#
    #vmax = ceil(2*wigner_mat.max())/2
    handle = ax.contourf(xvec, xvec, qt.wigner(rho,xvec,xvec), 100, vmax = vmax, vmin = -vmax, cmap=get_cmap("RdBu"))
    #ax.contour(xvec, xvec, qt.wigner(rho,xvec,xvec), 10, vmax = vmax, vmin = -vmax, colors='k', alpha=0.1)
    ax.set_aspect("equal"); ax.tick_params(labelsize=14)
    ax.set_xlabel(r"$x$", fontsize=14); ax.set_ylabel(r"$p$", fontsize=14)
    if cbar:
        colorbar(handle)
    return ax

def plot_wigners(rho_list):
    if len(rho_list) > 1:
        fig, ax = subplots(1, len(rho_list),figsize=(17,6))
        for j,rho in enumerate(rho_list):
            xvec = linspace(-sqrt(rho.dims[0][0]), sqrt(rho.dims[0][0]), 100)
            ax[j].contourf(xvec, xvec, qt.wigner(rho,xvec,xvec), 100, norm=clr.Normalize(-0.25,0.25), cmap=get_cmap("RdBu"))
            ax[j].set_aspect("equal"); ax[j].tick_params(labelsize=14)
            ax[j].set_xlabel(r"$x$", fontsize=14); ax[j].set_ylabel(r"$p$", fontsize=14)
    else:
        rho = rho_list[0]
        xvec = linspace(-sqrt(rho.dims[0][0]), sqrt(rho.dims[0][0]), 100)
        contourf(xvec, xvec, qt.wigner(rho,xvec,xvec), 100, norm=clr.Normalize(-0.25,0.25), cmap=get_cmap("RdBu"))
        gca().set_aspect("equal"); tick_params(labelsize=14)
        xlabel(r"$x$", fontsize=14); ylabel(r"$p$", fontsize=14)

def truncation_bar(rho):
    f, ax = subplots()
    ax.bar(range(rho.shape[0]),[real(rho[i,i]) for i in range(rho.shape[0])])

def truncation_check(rho_list, ratio=0.4, thres=0.005):
    if isinstance(rho_list, list)==False: rho_list = [rho_list]
    return sum([sum([real(rho[i,i]) for i in range(int(floor((1-ratio)*rho.shape[0])),rho.shape[0])]) > thres for rho in rho_list])

def nG_h(x):
    x = 2*x+1e-10 #Because of the convention difference, and avoid NaN
    return (x+0.5)*log(x+0.5)-(x-0.5)*log(x-0.5)

def nG(rho, var):
    if len(var) == 2:
        return nG_h(sqrt(det(var))) - qt.entropy.entropy_vn(rho)
    #if len(var) == 4:
        #dplus = sqrt((det(var)+sqrt(det(var)**2-4*eye(4)))/2)
        #dminus = sqrt((det(var)-sqrt(det(var)**2-4*eye(4)))/2)
        #return nG_h(dplus)+nG(dminus)- qt.entropy.entropy_vn(rho)










#
