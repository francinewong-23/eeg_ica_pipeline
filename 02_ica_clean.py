import mne
from mne.preprocessing import ICA
import matplotlib.pyplot as plt

data_path = mne.datasets.sample.data_path()
raw_fname = data_path / 'MEG' / 'sample' / 'sample_audvis_raw.fif'
raw = mne.io.read_raw_fif(raw_fname, preload=True)

raw.pick_types(eeg=True, eog=True, stim=False)

raw.set_eeg_reference('average', projection=True).apply_proj()

raw_filtered = raw.copy().filter(l_freq=1.0, h_freq=40.0, fir_design='firwin')
ica = ICA(n_components=15, max_iter='auto', random_state=42)
ica.fit(raw_filtered)

# AUTOMATED EYE BLINK IDENTIFICATION VIA EOG CORRELATION
eog_indices, eog_scores = ica.find_bads_eog(raw_filtered, ch_name='EOG 061')
ica.exclude = eog_indices

print("\n=== AUTOMATED ICA ARTIFACT DETECTION ===")
print(f"Automatically identified bad EOG components: {ica.exclude}")

raw_cleaned = raw_filtered.copy()
ica.apply(raw_cleaned)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True, sharey=True)

data_orig, times = raw_filtered['EEG 001', :]
data_clean, _ = raw_cleaned['EEG 001', :]

ax1.plot(times[:6000], data_orig[0][:6000] * 1e6, color='crimson', label='Raw (With Eye Blinks)')
ax1.set_title("EEG Signal BEFORE ICA Cleaning (Frontal Channel EEG 001)")
ax1.set_ylabel("Amplitude (µV)")
ax1.legend(loc='upper right')
ax1.grid(True)

ax2.plot(times[:6000], data_clean[0][:6000] * 1e6, color='teal', label='ICA Cleaned')
ax2.set_title("EEG Signal AFTER ICA Cleaning (Eye Blinks Flattened)")
ax2.set_xlabel("Time (seconds)")
ax2.set_ylabel("Amplitude (µV)")
ax2.legend(loc='upper right')
ax2.grid(True)

plt.tight_layout()
plt.show(block=True)