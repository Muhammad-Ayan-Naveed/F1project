import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import numpy as np

# ── Load Data ──────────────────────────────────────────────
fastf1.Cache.enable_cache('cache')

session = fastf1.get_session(2023, 'Japanese Grand Prix', 'R')
session.load(telemetry=True, weather=False, messages=False)

# ── Get track map from fastest lap ─────────────────────────
fastest = session.laps.pick_fastest()
tel = fastest.get_telemetry()

x = tel['X'].values
y = tel['Y'].values

# ── Get driver positions at lap 10 ─────────────────────────
lap_number = 10
drivers = session.drivers

fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

# Draw track
ax.plot(x, y, color='white', linewidth=3, zorder=1)

# Plot each driver dot
for drv in drivers:
    try:
        drv_laps = session.laps.pick_driver(drv)
        lap = drv_laps[drv_laps['LapNumber'] == lap_number]
        if lap.empty:
            continue

        tel_drv = lap.iloc[0].get_telemetry()
        if tel_drv.empty:
            continue

        # Take midpoint of telemetry as position
        mid = len(tel_drv) // 2
        px = tel_drv['X'].iloc[mid]
        py = tel_drv['Y'].iloc[mid]

        # Get team color
        try:
            color = fastf1.plotting.get_driver_color(drv, session)
        except:
            color = 'white'

        abbr = session.get_driver(drv)['Abbreviation']

        ax.scatter(px, py, color=color, s=120, zorder=3)
        ax.text(px, py + 80, abbr, color='white',
                fontsize=7, ha='center', zorder=4)

    except Exception as e:
        continue

# ── Leaderboard ────────────────────────────────────────────
results = session.results[['Abbreviation', 'Position']].sort_values('Position')
leaderboard = '\n'.join(
    f"{int(row.Position)}. {row.Abbreviation}"
    for _, row in results.iterrows()
    if int(row.Position) <= 20
)

ax.text(1.02, 0.95, "Leaderboard", transform=ax.transAxes,
        color='white', fontsize=10, fontweight='bold', va='top')
ax.text(1.02, 0.88, leaderboard, transform=ax.transAxes,
        color='white', fontsize=8, va='top', family='monospace')

# ── Labels ─────────────────────────────────────────────────
ax.set_title('F1 Race Replay — Japanese GP 2023 | Lap 10',
             color='white', fontsize=13, pad=15)
ax.axis('off')
plt.tight_layout()
plt.savefig('lap10_snapshot.png', dpi=150,
            bbox_inches='tight', facecolor='#1a1a2e')
plt.show()
print("Saved as lap10_snapshot.png")