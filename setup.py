from setuptools import setup
from glob import glob

package_name = 'npu_com'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/'+package_name+'/launch',glob('launch/*'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='demons',
    maintainer_email='2536890272Carl@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'com = npu_com.com:main'
        ],
    },
)
