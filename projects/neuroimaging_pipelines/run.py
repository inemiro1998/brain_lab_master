from projects.neuroimaging_pipelines.pipeline import PipelinefMRI

paths = {'input_path': '/home/brainlab/Desktop/Nichols/DMR_MRIdata',
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
         't1_relative_path':'t1.nii.gz',
         'fmri_relative_path':'fmri.nii',
         'mask_mni_path': '/home/brainlab/Desktop/Rudas/Data/Propofol/MNI152_T1_2mm_brain_mask.nii.gz'}

parameters = {'fwhm': 8,
              'tr': 2,
              'init_volume': 6,
              'iso_size': 2,
              'low_pass': 0.1,
              'high_pass': 0.01}

subject_list = ['c001',
                'c002',
                'c005',
                'c006',
                'c007',
                'c008',
                'c009',
                'c010',
                'c012',
                'c013',
                'c015',
                'c016',
                'c017',
                'c018',
                'c019',
                's002',
                's005',
                's006',
                's009',
                's011',
                's017',
                's018',
                's019',
                's020',
                'si006',
                'si009']

pipeline = PipelinefMRI(paths=paths, parameters=parameters, subject_list=subject_list)
pipeline.run()
