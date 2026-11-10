AUDIO = "final_mix_15.wav"
_R = json.load(open("results15.json"))
_c = pd.read_csv("sim15.csv")
STARTS = list(_c["start"])                 # "YYYY-MM" for each of the 228 rounds
WIN = [bool(v) for v in _c["win"]]         # True = ALL-IN ahead after 12 months
NR = len(WIN)
L_WINS = _R["lump_wins"]; D_WINS = NR - L_WINS; AVG_GAP = _R["avg_gap"]
WORST = _R["worst_for_lump"]               # the worst starting month for ALL-IN
W_L, W_D = WORST["lump12"], WORST["drip12"]
W_Y, W_M = int(WORST["start"][:4]), int(WORST["start"][5:])
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
STREAK_N, STREAK_A, STREAK_B = _R["longest_drip_streak"]
PL = np.array(_R["worst_paths"]["lump"], float); PD_ = np.array(_R["worst_paths"]["drip"], float)
assert L_WINS == 177 and D_WINS == 51 and AVG_GAP == 533 and STREAK_N == 19 and WORST["start"] == "2008-06"
assert round(W_L, -2) == 6900 and 9600 <= W_D < 9700
import rocco as _rk


def ri(ym):
    return STARTS.index(ym)
