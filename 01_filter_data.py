import mne
import matplotlib.pyplot as plt

data_path = mne.datasets.sample.data_path()
raw_fname = data_path / 'MEG' / 'sample' / 'sample_audvis_raw.fif'

raw = mne.io.read_raw_fif(raw_fname, preload=True)
raw.pick_types(eeg=True, eog=True, stim=False)

montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage, on_missing='ignore')

raw_ref = raw.copy().set_eeg_reference('average', projection=True)
raw_ref.apply_proj()

raw_filtered = raw_ref.copy().filter(l_freq=1.0, h_freq=40.0, fir_design='firwin')

raw_filtered.notch_filter(freqs=60.0, fir_design='firwin')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

raw.plot_psd(fmax=80, ax=ax1, show=False)
ax1.set_title("BEFORE Filtering (Raw Spectrum)")

raw_filtered.plot_psd(fmax=80, ax=ax2, show=False)
ax2.set_title("AFTER Filtering (Clean 1-40 Hz Spectrum with 60 Hz Notch)")

plt.tight_layout()
plt.show(block=True)