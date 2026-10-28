import polars as pl
import matplotlib.pyplot as plt
import numpy as np

VIOLET = 0
RED = 1
ORANGE = 2
YELLOW = 3
BLUE = 4
GREEN = 5

charge_of_electron = 1.60e-19
speed_of_light = 3.00e8

#wip
def plot():
    # improper plot

    fig, ax = plt.subplots()
    fig.suptitle("Violet LED")

    x = All_LED[VIOLET]["I/A"].to_numpy()
    y = All_LED[VIOLET]["V/V"].to_numpy()

    m, c = np.polyfit(x, y, 1)

    xs = np.linspace(0, np.max(x), 2)
    ys = m * xs + c

    xs_range = np.max(xs) - np.min(xs)
    ys_range = np.max(ys) - np.min(ys)

    xf = np.linspace(np.min(xs) - 0.1 * xs_range, np.max(xs) + 0.1 * xs_range, 2)
    yf = m * xf + c

    ax.scatter(x, y, color="violet", label="Violet LED")
    ax.set_xlabel("I/mA")
    ax.set_ylabel("V/V")

    ax.set_xlim(np.min(xs) - 0.1 * xs_range, np.max(xs) + 0.1 * xs_range)

    y_range = np.max(ys) - np.min(ys)
    ax.set_ylim(np.min(ys) - 0.1 * y_range, np.max(ys) + 0.1 * y_range)

    ax.plot(xf, yf, color="violet", label="Violet LED Linear Regression")
    ax.legend()

    plt.show()

    # stoping plot for now


if __name__ == "__main__":
    LED_1_violet = pl.read_excel("Plank's_Constant_intro_cycle_data.xlsx", sheet_name="Data", table_name="LED_1_violet")
    LED_2_red = pl.read_excel("Plank's_Constant_intro_cycle_data.xlsx", sheet_name="Data", table_name="LED_2_red")
    LED_3_orange = pl.read_excel("Plank's_Constant_intro_cycle_data.xlsx", sheet_name="Data", table_name="LED_3_orange")
    LED_4_yellow = pl.read_excel("Plank's_Constant_intro_cycle_data.xlsx", sheet_name="Data", table_name="LED_4_yellow")
    LED_5_blue = pl.read_excel("Plank's_Constant_intro_cycle_data.xlsx", sheet_name="Data", table_name="LED_5_blue")
    LED_6_green = pl.read_excel("Plank's_Constant_intro_cycle_data.xlsx", sheet_name="Data", table_name="LED_6_green")

    All_LED = [LED_1_violet,
              LED_2_red,
              LED_3_orange,
              LED_4_yellow,
              LED_5_blue,
              LED_6_green]

    LED_wavelengths = pl.read_excel("Plank's_Constant_intro_cycle_data.xlsx", sheet_name="Data", table_name="LED_wavelengths")

    # Converting Units
    for LED_number in range(0, len(All_LED)):
        All_LED[LED_number] = All_LED[LED_number].select(
            (pl.col("I/mA") / 1000).alias("I/A"),
            pl.col("V/V")
        ).sort("I/A").tail(8)


    LED_wavelengths = LED_wavelengths.select(
        pl.col("LED number").alias("LED_number"),
        (pl.col("lambda/nm") / 1e9).alias("wavelength/m"),
        (pl.col("FWHM/nm") / 1e9).alias("FWHM/m")
    )

    Threshold_V = []

    for LED in All_LED:
        x = LED["I/A"].to_numpy()
        y = LED["V/V"].to_numpy()
        m, c = np.polyfit(x, y, 1)

        Threshold_V.append(c)

    wavelengths = LED_wavelengths["wavelength/m"].to_numpy()

    new_x = 1/wavelengths

    m, c = np.polyfit(new_x, Threshold_V, 1)

    h = m*charge_of_electron/speed_of_light
    print(h)

