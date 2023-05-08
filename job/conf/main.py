import argparse
from xml.dom import minidom as md
from xml.etree import ElementTree as ET

import pandas as pd
import yaml
from box import Box


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-c",
        "--conf",
        type=str,
        required=True,
        metavar="CONF",
        help="URLなどの設定を記載したconfig.yaml",
    )
    ap.add_argument(
        "-l",
        "--load",
        type=str,
        required=True,
        metavar="LOAD",
        help="負荷変動を記載したload.csv",
    )
    ap.add_argument(
        "-o",
        "--output",
        type=str,
        default="test.jmx",
        metavar="OUTPUT",
        help="出力するアウトプットファイルのファイル名(default:test.jmx)",
    )
    return ap.parse_args()


def read_conf(conf_file):
    config = None
    with open(conf_file, "r") as f:
        config = Box(yaml.safe_load(f))
        pass
    return config


def saveJMX(jmx, file_path):
    jmx = ET.tostring(jmx, encoding="UTF-8")
    jmx = md.parseString(jmx)
    with open(file_path, "w") as f:
        jmx.writexml(f, encoding="utf-8", newl="\n", indent="", addindent="  ")
        pass
    return


def printJMX(jmx):
    fn = "test.jmx"
    saveJMX(jmx, fn)
    with open(fn, "r") as f:
        print(f.read())
        pass
    return


def createJMX(domain, port, path, threads, load, file_path, hasCounter=True):
    jmx = _createTestPlan()
    _createThreadGroup(jmx, threads)
    _createHTTPSampler(jmx, domain, port, path, hasCounter)
    if hasCounter:
        _createCounterConfig(jmx)
        pass
    _createVariableThroughputTimer(jmx, load)

    saveJMX(jmx, file_path)
    printJMX(jmx)
    return jmx


def _getHashTree(jmx, N=20):
    ht = jmx.find("hashTree")
    hashTree = None
    if ht is None:
        hashTree = ET.SubElement(jmx, "hashTree")
    else:
        for i in range(N):
            tmp = ht.find("hashTree")
            if tmp is None:
                hashTree = ET.SubElement(ht, "hashTree")
                break
            ht = tmp
            pass
        pass
    if hashTree is None:
        hashTree = ET.SubElement(ht, "hashTree")
        pass
    return hashTree


def _createTestPlan():
    jmx = ET.Element("jmeterTestPlan", version="1.2", properties="5.0", jmeter="5.5")
    hash = _getHashTree(jmx)
    tp = "TestPlan"

    # Create the Test Plan element
    testPlan = ET.SubElement(
        hash,
        "TestPlan",
        guiclass="TestPlanGui",
        testclass="TestPlan",
        testname="Test Plan",
        enabled="true",
    )

    # Add Test Plan element properties
    ET.SubElement(testPlan, "stringProp", name=f"{tp}.comments")
    p2 = ET.SubElement(testPlan, "boolProp", name=f"{tp}.functional_mode")
    p2.text = "false"
    p3 = ET.SubElement(testPlan, "boolProp", name=f"{tp}.tearDown_on_shutdown")
    p3.text = "true"
    p4 = ET.SubElement(testPlan, "boolProp", name=f"{tp}.serialize_threadgroups")
    p4.text = "false"

    # Create User Defined Variables element
    userDefinedVariables = ET.SubElement(
        testPlan,
        "elementProp",
        name=f"{tp}.user_defined_variables",
        elementType="Arguments",
        guiclass="ArgumentsPanel",
        testclass="Arguments",
        testname="User Defined Variables",
        enabled="true",
    )
    ET.SubElement(userDefinedVariables, "collectionProp", name="Arguments.arguments")

    # Create User Defined Classpath element
    ET.SubElement(testPlan, "stringProp", name=f"{tp}.user_define_classpath")

    return jmx


def _createThreadGroup(jmx, threads):
    hash = _getHashTree(jmx)
    tg = "ThreadGroup"

    threadGroup = ET.SubElement(
        hash,
        tg,
        guiclass="ThreadGroupGui",
        testclass=tg,
        testname="Test Thread Group",
        enabled="true",
    )
    p1 = ET.SubElement(threadGroup, "stringProp", name=f"{tg}.on_sample_error")
    p1.text = "continue"
    loopController = ET.SubElement(
        threadGroup,
        "elementProp",
        name=f"{tg}.main_controller",
        elementType="LoopController",
        guiclass="LoopControlPanel",
        testclass="LoopController",
        testname="Loop Controller",
        enabled="true",
    )
    p2 = ET.SubElement(
        loopController, "boolProp", name="LoopController.continue_forever"
    )
    p2.text = "false"
    p3 = ET.SubElement(loopController, "intProp", name="LoopController.loops")
    p3.text = "-1"
    p4 = ET.SubElement(threadGroup, "stringProp", name=f"{tg}.num_threads")
    p4.text = str(threads)
    p5 = ET.SubElement(threadGroup, "stringProp", name=f"{tg}.ramp_time")
    p5.text = "0"
    p6 = ET.SubElement(threadGroup, "boolProp", name=f"{tg}.scheduler")
    p6.text = "false"
    p7 = ET.SubElement(threadGroup, "stringProp", name=f"{tg}.duration")
    p7.text = ""
    p8 = ET.SubElement(threadGroup, "stringProp", name=f"{tg}.delay")
    p8.text = ""
    p9 = ET.SubElement(
        threadGroup, "boolProp", name=f"{tg}.same_user_on_next_iteration"
    )
    p9.text = "true"
    return


def _createHTTPSampler(jmx, domain, port, path, hasCounter=True):
    hash = _getHashTree(jmx)
    hs = "HTTPSampler"

    # Create the HTTPSamplerProxy element
    httpSampler = ET.SubElement(
        hash,
        "HTTPSamplerProxy",
        guiclass="HttpTestSampleGui",
        testclass="HTTPSamplerProxy",
        testname="HTTP Request",
        enabled="true",
    )

    # Add child elements to the HTTPSamplerProxy element
    elementProp = ET.SubElement(
        httpSampler,
        "elementProp",
        name=f"{hs}.Arguments",
        elementType="Arguments",
        guiclass="HTTPArgumentsPanel",
        testclass="Arguments",
        testname="User Defined Variables",
        enabled="true",
    )
    ET.SubElement(elementProp, "collectionProp", name="Arguments.arguments")
    p1 = ET.SubElement(httpSampler, "stringProp", name=f"{hs}.domain")
    p1.text = f"{domain}"
    p2 = ET.SubElement(httpSampler, "stringProp", name=f"{hs}.port")
    p2.text = f"{port}"
    p3 = ET.SubElement(httpSampler, "stringProp", name=f"{hs}.protocol")
    p3.text = "http"
    ET.SubElement(httpSampler, "stringProp", name=f"{hs}.contentEncoding")
    p5 = ET.SubElement(httpSampler, "stringProp", name=f"{hs}.path")
    p5.text = f"{path}"
    if hasCounter:
        if "?" in p5.text:
            p5.text += "&serial=${serial_counter}&no_db=true"
        else:
            p5.text += "?serial=${serial_counter}&no_db=true"
            pass
        pass

    p6 = ET.SubElement(httpSampler, "stringProp", name=f"{hs}.method")
    p6.text = "GET"
    p7 = ET.SubElement(httpSampler, "boolProp", name=f"{hs}.follow_redirects")
    p7.text = "true"
    p8 = ET.SubElement(httpSampler, "boolProp", name=f"{hs}.auto_redirects")
    p8.text = "false"
    p9 = ET.SubElement(httpSampler, "boolProp", name=f"{hs}.use_keepalive")
    p9.text = "true"
    p10 = ET.SubElement(httpSampler, "boolProp", name=f"{hs}.DO_MULTIPART_POST")
    p10.text = "false"
    ET.SubElement(httpSampler, "stringProp", name=f"{hs}.embedded_url_re")
    ET.SubElement(httpSampler, "stringProp", name=f"{hs}.connect_timeout")
    ET.SubElement(httpSampler, "stringProp", name=f"{hs}.response_timeout")
    return


def _createCounterConfig(jmx):
    hash = _getHashTree(jmx)
    cc = "CounterConfig"

    # Create the CounterConfig element
    counterConfig = ET.SubElement(
        hash,
        "CounterConfig",
        guiclass="CounterConfigGui",
        testclass="CounterConfig",
        testname="serial_counter",
        enabled="true",
    )

    # Add child elements to the CounterConfig element
    p1 = ET.SubElement(counterConfig, "stringProp", name=f"{cc}.start")
    p1.text = "1"
    p2 = ET.SubElement(counterConfig, "stringProp", name=f"{cc}.end")
    p2.text = "999999999"
    p3 = ET.SubElement(counterConfig, "stringProp", name=f"{cc}.incr")
    p3.text = "1"
    p4 = ET.SubElement(counterConfig, "stringProp", name=f"{cc}.name")
    p4.text = "serial_counter"
    p5 = ET.SubElement(counterConfig, "stringProp", name=f"{cc}.format")
    p5.text = "000000000"
    p6 = ET.SubElement(counterConfig, "boolProp", name=f"{cc}.per_user")
    p6.text = "false"
    return


def _createVariableThroughputTimer(jmx, load):
    hash = jmx.find("hashTree")
    for _ in range(2):
        hash = hash.find("hashTree")
        pass

    # Create the kg.apc.jmeter.timers.VariableThroughputTimer element
    timer = ET.SubElement(
        hash,
        "kg.apc.jmeter.timers.VariableThroughputTimer",
        guiclass="kg.apc.jmeter.timers.VariableThroughputTimerGui",
        testclass="kg.apc.jmeter.timers.VariableThroughputTimer",
        testname="jp@gc - Throughput Shaping Timer",
        enabled="true",
    )

    # Create the load_profile element and add it as a child to the timer element
    loadProfile = ET.SubElement(timer, "collectionProp", name="load_profile")

    # Create the four collectionProp elements and add them as children to the load_profile element
    for _, s in load.iterrows():
        collectionProp = ET.SubElement(loadProfile, "collectionProp", name="")
        p1 = ET.SubElement(collectionProp, "stringProp", name="")
        p1.text = str(s.start)
        p2 = ET.SubElement(collectionProp, "stringProp", name="")
        p2.text = str(s.end)
        p3 = ET.SubElement(collectionProp, "stringProp", name="")
        p3.text = str(s.duration)
        pass
    return


def main():
    args = get_args()
    conf = read_conf(args.conf)
    load = pd.read_csv(args.load)
    createJMX(conf.domain, conf.port, conf.path, conf.threads, load, args.output)
    return


if __name__ == "__main__":
    main()
