from projects.neuroimaging_pipelines.pipeline import PipelinefMRI

paths = {'input_path': '/home/brainlab/Desktop/Rudas/Data/Propofol/Recovery/Task/',
         'template_spm_path': '/home/brainlab/Desktop/Rudas/Data/Parcellation/TPM.nii',
         'mcr_path': '/home/brainlab/Desktop/Rudas/Tools/MCR/v713',
         'spm_path': '/home/brainlab/Desktop/Rudas/Tools/spm12_r7487/spm12/run_spm12.sh',
         'image_parcellation_path': ['/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/Auditory/Auditory_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/CinguloOperc/CinguloOperc_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/CinguloParietal/CinguloParietal_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/Default/Default_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/DorsalAttn/DorsalAttn_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/FrontoParietal/FrontoParietal_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/None/None_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/RetrosplenialTemporal/RetrosplenialTemporal_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/SMhand/SMhand_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/SMmouth/SMmouth_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/VentralAttn/VentralAttn_parcellation_5.nii',
                                     '/home/brainlab/Desktop/Rudas/Data/Parcellation/rsn_parcellations/Visual/Visual_parcellation_5.nii'],
         'labels_parcellation_path': None,
         't1_relative_path':'t1.nii',
         'fmri_relative_path':'fmri.nii',
         'mask_mni_path': '/home/brainlab/Desktop/Rudas/Data/Propofol/MNI152_T1_2mm_brain_mask.nii.gz'}

parameters = {'fwhm': 8,
              'tr': 2,
              'init_volume': 6,
              'iso_size': 2,
              'low_pass': 0.1,
              'high_pass': 0.01}

subject_list = ['2014_05_02_02CB',
                '2014_05_16_16RA',
                '2014_05_30_30AQ',
                '2014_07_04_04HD',
                '2014_07_04_04SG',
                '2014_08_13_13CA',
                '2014_10_08_08BC',
                '2014_10_08_08VR',
                '2014_10_22_22CY',
                '2014_10_22_22TK',
                '2014_11_17_17EK',
                '2014_11_17_17NA',
                '2014_11_19_19SA',
                '2014_11_19_AK',
                '2014_11_25.25JK',
                '2014_11_27_27HF',
                '2014_12_10_10JR']

pipeline = PipelinefMRI(paths=paths, parameters=parameters, subject_list=subject_list)
pipeline.run()
