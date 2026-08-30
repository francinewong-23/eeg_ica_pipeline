import mne
from mne.preprocessing import ICA
import numpy as np

data_path = mne.datasets.sample.data_path()
raw_fname = data_path / 'MEG' / 'sample' / 'sample_audvis_raw.fif'
raw = mne.io.read_raw_fif(raw_fname, preload=True)
raw.pick_types(eeg=True, eog=True, stim=False)
raw.set_eeg_reference('average', projection=True).apply_proj()

raw_filtered = raw.copy().filter(l_freq=1.0, h_freq=40.0, fir_design='firwin')

ica = ICA(n_components=15, max_iter='auto', random_state=42)
ica.fit(raw_filtered)

eog_indices, _ = ica.find_bads_eog(raw_filtered, ch_name='EOG 061')
ica.exclude = eog_indices

raw_cleaned = raw_filtered.copy()
ica.apply(raw_cleaned)

raw_data, _ = raw_filtered['EEG 001', :]
clean_data, _ = raw_cleaned['EEG 001', :]

var_raw = np.var(raw_data)
var_clean = np.var(clean_data)
var_reduction = ((var_raw - var_clean) / var_raw) * 100

# Metric B: Signal-to-Noise Ratio (SNR in dB)
noise = raw_data - clean_data
snr_initial = 10 * np.log10(np.mean(raw_data ** 2) / np.mean(noise ** 2))
snr_cleaned = 10 * np.log10(np.mean(clean_data ** 2) / np.mean(noise ** 2))
snr_gain = snr_cleaned - snr_initial

print("\n" + "="*45)
print("   QUANTITATIVE SIGNAL CLEANING RESULTS")
print("="*45)
print(f"Bad Components Removed : {ica.exclude}")
print(f"Original Signal Variance: {var_raw:.2e}")
print(f"Cleaned Signal Variance : {var_clean:.2e}")
print(f"Artifact Variance Cut   : {var_reduction:.2f}%")
print(f"SNR Improvement Gain    : {snr_gain:+.2f} dB")
print("="*45)