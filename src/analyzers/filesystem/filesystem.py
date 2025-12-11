#!/usr/bin/env python3
"""Filesystem analysis from sosreport"""

from pathlib import Path
from utils.logger import Logger


class FilesystemAnalyzer:
    """Analyze filesystem configuration and usage from sosreport"""
    
    def analyze_mounts(self, base_path: Path) -> dict:
        """Analyze mount points and fstab"""
        Logger.debug("Analyzing mounts and fstab")
        
        data = {}
        
        # fstab
        fstab = base_path / 'etc' / 'fstab'
        if fstab.exists():
            data['fstab'] = fstab.read_text()
        
        # Current mounts
        mounts = base_path / 'proc' / 'mounts'
        if mounts.exists():
            data['proc_mounts'] = mounts.read_text()
        
        # Mount command output
        mount_cmd = base_path / 'sos_commands' / 'filesys' / 'mount_-l'
        if mount_cmd.exists():
            data['mount_output'] = mount_cmd.read_text()
        
        # Mountinfo
        mountinfo = base_path / 'proc' / 'self' / 'mountinfo'
        if mountinfo.exists():
            data['mountinfo'] = mountinfo.read_text()
        
        return data
    
    def analyze_lvm(self, base_path: Path) -> dict:
        """Analyze LVM configuration"""
        Logger.debug("Analyzing LVM configuration")
        
        data = {}
        
        # PV display
        pvs = base_path / 'sos_commands' / 'lvm2' / 'pvs_-a_-o_pv_all'
        if pvs.exists():
            data['pvs'] = pvs.read_text()
        
        # VG display
        vgs = base_path / 'sos_commands' / 'lvm2' / 'vgs_-a_-o_vg_all'
        if vgs.exists():
            data['vgs'] = vgs.read_text()
        
        # LV display
        lvs = base_path / 'sos_commands' / 'lvm2' / 'lvs_-a_-o_lv_all'
        if lvs.exists():
            data['lvs'] = lvs.read_text()
        
        # LVM config
        lvm_conf = base_path / 'etc' / 'lvm' / 'lvm.conf'
        if lvm_conf.exists():
            data['lvm_conf'] = lvm_conf.read_text()
        
        return data
    
    def analyze_disk_usage(self, base_path: Path) -> dict:
        """Analyze disk usage"""
        Logger.debug("Analyzing disk usage")
        
        data = {}
        
        # df output
        df_cmd = base_path / 'sos_commands' / 'filesys' / 'df_-al_-x_autofs'
        if not df_cmd.exists():
            df_cmd = base_path / 'df'
        if df_cmd.exists():
            data['df'] = df_cmd.read_text()
        
        # df inodes
        df_inodes = base_path / 'sos_commands' / 'filesys' / 'df_-ali'
        if df_inodes.exists():
            data['df_inodes'] = df_inodes.read_text()
        
        # Disk stats
        diskstats = base_path / 'proc' / 'diskstats'
        if diskstats.exists():
            data['diskstats'] = diskstats.read_text()
        
        return data
    
    def analyze_filesystems(self, base_path: Path) -> dict:
        """Analyze filesystem types and features"""
        Logger.debug("Analyzing filesystems")
        
        data = {}
        
        # Filesystem types
        filesystems = base_path / 'proc' / 'filesystems'
        if filesystems.exists():
            data['filesystems'] = filesystems.read_text()
        
        # XFS info
        xfs_info_dir = base_path / 'sos_commands' / 'xfs'
        if xfs_info_dir.exists():
            xfs_files = {}
            for xfs_file in xfs_info_dir.glob('xfs_info_*'):
                try:
                    xfs_files[xfs_file.name] = xfs_file.read_text()
                except Exception:
                    pass
            if xfs_files:
                data['xfs_info'] = xfs_files
        
        # Ext filesystem info
        ext_info_dir = base_path / 'sos_commands' / 'filesys'
        if ext_info_dir.exists():
            ext_files = {}
            for ext_file in ext_info_dir.glob('dumpe2fs_*'):
                try:
                    ext_files[ext_file.name] = ext_file.read_text()[:5000]  # Limit size
                except Exception:
                    pass
            if ext_files:
                data['ext_info'] = ext_files
        
        # Blkid output
        blkid = base_path / 'sos_commands' / 'block' / 'blkid_-c_.dev.null'
        if not blkid.exists():
            blkid = base_path / 'sos_commands' / 'filesys' / 'blkid'
        if blkid.exists():
            data['blkid'] = blkid.read_text()
        
        return data
