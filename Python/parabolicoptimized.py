import numpy as np
from scipy import constants
from sympy import symbols, Eq, solve, sin, cos
import matplotlib.pyplot as plt
import pandas as pd


def saveSolution(solution, initial_angle, deflection_angle):

    variables = {"t": solution["solt"],
                 "x": solution["solx"],
                 "y": solution["soly"],
                 "z": solution["solz"],
                 "v": solution["solv"],
                 "v_x_0": solution["solvx0"],
                 "v_y_0": solution["solvy0"],
                 "v_z_0": solution["solvz0"],
                 "v_x": solution["solvx"],
                 "v_y": solution["solvy"],
                 "v_z": solution["solvz"],
                 "v_t": solution["solvt"]}
    df = pd.DataFrame(variables)
    df.to_csv(
        "results{:.0f}_&{:.0f}.csv".format(initial_angle, deflection_angle))


def plotSolution(solution, initial_angle, deflection_angle, xzmax, yzmax, zmax, r):
    fig = plt.figure()
    fig.suptitle('Trajectory and velocities of the projectile')

    ax1 = fig.add_subplot(3, 2, 2)
    ax1.title.set_text("v_x")
    ax1.set_ylabel("v [m/s]")
    ax1.set_xlim(0, solution["solt"][-1])
    ax1.plot(solution["solt"], solution["solvx"], 'r', label="v_x")
    ax1.set_ylim(bottom=0, top=None)
    ax1.grid()

    ax2 = fig.add_subplot(3, 2, 4)
    ax2.title.set_text("v_y")
    ax2.sharex(ax1)
    ax2.sharey(ax1)
    ax2.set_ylabel("v [m/s]")
    ax2.plot(solution["solt"], solution["solvy"], 'g', label="v_y")
    ax2.set_ylim(bottom=0, top=None)
    ax2.grid()

    ax3 = fig.add_subplot(3, 2, 6)
    ax3.title.set_text("v_z")
    ax3.grid()
    ax3.sharex(ax2)
    ax3.set_ylabel("v [m/s]")
    ax3.set_xlabel("t [s]")
    ax3.plot(solution["solt"], solution["solvz"], label="v_z")

    rmax = max([max(solution["solx"]), max(solution["soly"]), max(solution["solz"])])
    # Second subplot
    ax4 = fig.add_subplot(3, 2, (1, 5), projection='3d')
    ax4.axes.set_xlim3d(left=0, right=int(rmax))
    ax4.axes.set_ylim3d(bottom=0, top=int(rmax))
    ax4.axes.set_zlim3d(bottom=0, top=int(rmax))
    ax4.set_title("Trajectory for \u03B1 = {:.1f}° , \u03B8 = {:.1f}°".format(initial_angle,
                                                                              deflection_angle))
    ax4.set_xlabel('x [m]')
    ax4.set_ylabel('y [m]')
    ax4.set_zlabel('z [m]')
    scatter = ax4.scatter(solution["solx"], solution["soly"], solution["solz"], c=solution["solv"], cmap='rainbow')
    ax4.plot3D(solution["solx"], solution["soly"], solution["solz"], 'k', linewidth=0.5)
    ax4.plot3D(solution["solx"], solution["soly"], 0, 'k--', linewidth=0.5)
    # ax4.plot3D(solx, [0]*len(solx), solz, 'k--', linewidth = 0.5)
    # ax4.plot3D([0]*len(soly), soly, solz, 'k--', linewidth = 0.5)
    ax4.plot3D([solution["solx"][int(0.1 * len(solution["solx"]))], solution["solx"][int(0.1 * len(solution["solx"]))]],
               [solution["soly"][int(0.1 * len(solution["solx"]))], solution["soly"][int(0.1 * len(solution["solx"]))]],
               [0, solution["solz"][int(0.1 * len(solution["solx"]))]], 'k--',
               linewidth=0.5)
    ax4.plot3D([solution["solx"][int(0.1 * len(solution["solx"]))], solution["solx"][int(0.1 * len(solution["solx"]))]],
               [0, solution["soly"][int(0.1 * len(solution["solx"]))]], [0, 0], 'k--',
               linewidth=0.5)
    cb = plt.colorbar(scatter, fraction=0.046, pad=0.08, location='left')
    cb.set_ticks([min(solution["solv"]), (min(solution["solv"]) + max(solution["solv"])) / 2, max(solution["solv"])])
    cb.set_ticklabels(["{:.1f} m/s".format(min(solution["solv"])),
                       "{:.1f} m/s".format((min(solution["solv"]) + max(solution["solv"])) / 2),
                       "{:.1f} m/s".format(max(solution["solv"]))])

    ax4.plot3D([xzmax, xzmax], [yzmax, yzmax], [0, zmax], 'k--', linewidth=0.5)
    ax4.plot3D([0, solution["solx"][-1]], [solution["soly"][-1], solution["soly"][-1]], [0, 0], 'k--', linewidth=0.5)
    ax4.plot3D([solution["solx"][-1], solution["solx"][-1]], [0, solution["soly"][-1]], [0, 0], 'k--', linewidth=0.5)
    ax4.scatter(xzmax, yzmax, zmax, color='r', s=7.5)
    ax4.text(xzmax, yzmax, 1.1 * zmax, "{:.1f} m".format(zmax))
    ax4.text(1.1 * solution["solx"][int(0.1 * len(solution["solx"]))],
             1.1 * solution["soly"][int(0.1 * len(solution["solx"]))],
             solution["solz"][int(0.1 * len(solution["solx"]))] / 2,
             "\u03B1 = {:.1f} °".format(initial_angle))
    ax4.text(1.3 * solution["solx"][int(0.1 * len(solution["solx"]))], 0, 0,
             "\u03B8 = {:.1f} °".format(deflection_angle))
    ax4.text(1.05*solution["solx"][-1], 1.05*solution["soly"][-1], 0,"r = {:.1f} m".format(r))
    ax4.view_init(20, 275)


def calculateTrajectory(mass=567, density=1.179, cross_area=0.07, initial_x=0, initial_y=0, initial_z=5000,
                        initial_v=150, initial_angle=0, deflection_angle=25, drag_coeff=0.25, times=(0, 60, 0.5)):
    m, t, t_0, x, y, z, alpha, theta, x_0, y_0, z_0, v_0, v, v_x, v_y, v_z, v_x_0, v_y_0, v_z_0, v_t, c_d, rho, A = symbols(
        'm t t_0 x y z alpha theta x_0 y_0 z_0 v_0 v v_x v_y v_z v_x_0 v_y_0 v_z_0 v_t c_ rho A')

    g = constants.g
    e = 2.71828
    pi = constants.pi
    rad_initial_angle = initial_angle * pi / 180
    rad_deflection_angle = deflection_angle * pi / 180
    time = np.arange(start=times[0], stop=times[1], step=times[2])
    print("\nCase of alpha = {:.1f} °".format(initial_angle))
    outputs = ["solx", "soly", "solz", "solv", "solvx", "solvy", "solvz", "solvx0", "solvy0", "solvz0", "solvt", "solt"]
    solution = {item: [] for item in outputs}

    terminal_vel = Eq(v_t, ((2 * m * g) / (c_d * rho * A)) ** 0.5)
    vel_x_0 = Eq(v_x_0, v_0 * cos(alpha) * cos(theta))
    vel_y_0 = Eq(v_y_0, v_0 * cos(alpha) * sin(theta))
    vel_z_0 = Eq(v_z_0, v_0 * sin(alpha))
    pos_x = Eq(x, x_0 + v_x_0 * v_t / g * (1 - e ** (-g * t / v_t)))
    pos_y = Eq(y, y_0 + v_y_0 * v_t / g * (1 - e ** (-g * t / v_t)))
    pos_z = Eq(z, z_0 + v_t / g * (v_z_0 + v_t) * (1 - e ** (- g * t / v_t)) - v_t * t)
    vel_x = Eq(v_x, v_x_0 * e ** (-g * t / v_t))
    vel_y = Eq(v_y, v_y_0 * e ** (-g * t / v_t))
    vel_z = Eq(v_z, v_z_0 * e ** (-g * t / v_t) - v_t * (1 - e ** (-g * t / v_t)))
    vel = Eq(v, (v_x ** 2 + v_y ** 2 + v_z ** 2) ** 0.5)

    for timestep in time:
        print("Solving time = {:.2f} s".format(timestep))
        terminal_vel_data = {m: mass,
                             rho: density,
                             A: cross_area,
                             c_d: drag_coeff}
        vel_x_0_data = {v_0: initial_v,
                        alpha: rad_initial_angle,
                        theta: rad_deflection_angle}
        vel_y_0_data = {v_0: initial_v,
                        alpha: rad_initial_angle,
                        theta: rad_deflection_angle}
        vel_z_0_data = {v_0: initial_v,
                        alpha: rad_initial_angle}
        pos_x_data = {x_0: initial_x,
                      t: timestep}
        pos_y_data = {y_0: initial_y,
                      t: timestep}
        pos_z_data = {z_0: initial_z,
                      t: timestep}
        vel_x_data = {t: timestep}
        vel_y_data = {t: timestep}
        vel_z_data = {t: timestep}

        sol = solve([terminal_vel.subs(terminal_vel_data),
                     pos_x.subs(pos_x_data),
                     pos_y.subs(pos_y_data),
                     pos_z.subs(pos_z_data),
                     vel,
                     vel_x_0.subs(vel_x_0_data),
                     vel_y_0.subs(vel_y_0_data),
                     vel_z_0.subs(vel_z_0_data),
                     vel_x.subs(vel_x_data),
                     vel_y.subs(vel_y_data),
                     vel_z.subs(vel_z_data)], (x, y, z, v, v_x_0, v_y_0, v_z_0, v_x, v_y, v_z, v_t), simplify=False,
                    rational=False, dict=True)

        if sol[0][z] > 0 and timestep < time[-1]:
            solution["solx"].append(sol[0][x])
            solution["soly"].append(sol[0][y])
            solution["solz"].append(sol[0][z])
            solution["solv"].append(sol[0][v])
            solution["solvx0"].append(sol[0][v_x_0])
            solution["solvy0"].append(sol[0][v_y_0])
            solution["solvz0"].append(sol[0][v_z_0])
            solution["solvx"].append(sol[0][v_x])
            solution["solvy"].append(sol[0][v_y])
            solution["solvz"].append(sol[0][v_z])
            solution["solvt"].append(sol[0][v_t])
            solution["solt"].append(timestep)

        elif sol[0][z] < 0 or timestep == time[-1]:

            zmax = max(solution["solz"])
            xzmax = solution["solx"][solution["solz"].index(max(solution["solz"]))]
            yzmax = solution["soly"][solution["solz"].index(max(solution["solz"]))]
            tzmax = solution["solt"][solution["solz"].index(max(solution["solz"]))]
            vzmax = solution["solv"][solution["solz"].index(max(solution["solz"]))]
            r = (max(solution["solx"])**2+max(solution["soly"])**2)**0.5
            print("============================ At apogee ============================")
            print("x = {:.1f} [m] y = {:.1f} [m] z = {:.1f} [m] t = {:.1f} [s] v = {:.1f} [m s-1]".format(xzmax,
                                                                                                          yzmax,
                                                                                                          zmax,
                                                                                                          tzmax,
                                                                                                          vzmax))
            print("===================================================================\n")
            print("============================ At impact ============================")
            print("x = {:.1f} [m] y = {:.1f} [m] z = {:.1f} [m] t = {:.1f} [s] v = {:.1f} [m s-1]".format(
                solution["solx"][-2],
                solution["soly"][-2],
                solution["solz"][-2],
                solution["solt"][-2],
                solution["solv"][-2]))
            print("===================================================================\n")
            print("========================== Miscelaneous ===========================")
            print("r = {:.1f} [m]".format(r))
            print("===================================================================\n")
            plotSolution(solution, initial_angle, deflection_angle, xzmax, yzmax, zmax, r)
            saveSolution(solution, initial_angle, deflection_angle)
            break


if __name__ == "__main__":
    calculateTrajectory()
    plt.show()

