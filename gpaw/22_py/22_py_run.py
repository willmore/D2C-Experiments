import sys
import os

from d2c.data.DAO import DAO
from d2c.data.CredStore import CredStore
from d2c.model.Role import Role
from d2c.model.Deployment import Deployment
from d2c.model.Action import Action
from d2c.model.DataCollector import DataCollector
from d2c.model.FileExistsFinishedCheck import FileExistsFinishedCheck
from d2c.EC2ConnectionFactory import EC2ConnectionFactory
from d2c.model.AMI import AMI
from d2c.model.InstanceType import InstanceType
from d2c.model.SSHCred import SSHCred
from d2c.logger import StdOutLogger
from TestConfig import TestConfig
from threading import Thread
from d2c.model.InstanceType import InstanceType
import random

def main(argv=None):
    
    conf = TestConfig("/home/willmore/test.conf")
    StdOutLogger().write("test123")        
    ec2ConnFactory = EC2ConnectionFactory(conf.awsCred.access_key_id, 
                                          conf.awsCred.secret_access_key, 
                                          StdOutLogger())
        
    masterOutDir = "./master/"
    
    sshCred = SSHCred('dirac', '/home/willmore/dirac.id_rsa')
    
    numHosts = 4
    script = "/home/dirac/amAu111BF4/22.py"
    doneFile = "/tmp/done.txt"
    startCmd = "nohup mpirun -np %d -hostfile /tmp/d2c.context gpaw-python %s &> experiment.out || true && date > %s &" % (numHosts, script, doneFile)


    instanceType = InstanceType("m1.xlarge", 2, 7500, 850, [])


    deployment = Deployment("22_py", 
                            ec2ConnFactory, 
                            roles=[
                                   Role("22_py", "master", 
                                        ami=AMI(amiId="ami-1396a167"), 
					count=1, 
                                        instanceType=instanceType,
					contextCred=sshCred,
                                        startActions=[Action(command=startCmd, 
                                                             sshCred=sshCred)],
                                        finishedChecks=[FileExistsFinishedCheck(fileName=doneFile, 
                                                                                sshCred=sshCred)],
                            
                                        dataCollectors=[DataCollector(source="/home/dirac", 
                                                                      destination=masterOutDir + "home_dir",
                                                                      sshCred=sshCred),
                                                        DataCollector(source="/opt/collectd/var/lib/collectd", 
                                                                      destination=masterOutDir + "collectd_stats",
                                                                      sshCred=sshCred)])])
    
    class Listener:  
        def notify(self, event):
            print "Deployment state changed to: " + event.newState
    
    deployment.addAnyStateChangeListener(Listener())
        
    thread = Thread(target=deployment.run)
    thread.start()
    thread.join()
    
    
if __name__ == "__main__":
    sys.exit(main())
