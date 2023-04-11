from xml.dom import minidom as md
from xml.etree import ElementTree as ET


def printJMX(jmx):
    jmx = ET.tostring(jmx, encoding="UTF-8")
    jmx = md.parseString(jmx)
    with open("test.jmx", "w") as f:
        jmx.writexml(f, encoding="utf-8", newl="\n", indent="", addindent="  ")
        pass
    with open("test.jmx", "r") as f:
        print(f.read())
        pass
    return


def createJMX(hasCounter=True):
    jmx = _createTestPlan()
    _createThreadGroup(jmx)
    _createHTTPSampler(jmx, hasCounter)
    if hasCounter:
        _createCounterConfig(jmx)
        pass
    _createVariableThroughputTimer(jmx)

    printJMX(jmx)
    return


def getHashTree(jmx):
    ht = jmx.find("hashTree")
    if ht is None:
        hashTree = ET.SubElement(jmx, "hashTree")
    else:
        for i in range(20):
            tmp = ht.find("hashTree")
            if tmp is None:
                hashTree = ET.SubElement(ht, "hashTree")
                break
            ht = tmp
            pass
        pass
    return hashTree


def _createTestPlan():
    jmx = ET.Element("jmeterTestPlan", version="1.2", properties="5.0", jmeter="5.5")
    hash = getHashTree(jmx)

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
    prop1 = ET.SubElement(testPlan, "stringProp", name="TestPlan.comments")
    prop2 = ET.SubElement(testPlan, "boolProp", name="TestPlan.functional_mode")
    prop2.text = "false"
    prop3 = ET.SubElement(testPlan, "boolProp", name="TestPlan.tearDown_on_shutdown")
    prop3.text = "true"
    prop4 = ET.SubElement(testPlan, "boolProp", name="TestPlan.serialize_threadgroups")
    prop4.text = "false"

    # Create User Defined Variables element
    userDefinedVariables = ET.SubElement(
        testPlan,
        "elementProp",
        name="TestPlan.user_defined_variables",
        elementType="Arguments",
        guiclass="ArgumentsPanel",
        testclass="Arguments",
        testname="User Defined Variables",
        enabled="true",
    )
    collectionProp1 = ET.SubElement(
        userDefinedVariables, "collectionProp", name="Arguments.arguments"
    )

    # Create User Defined Classpath element
    prop5 = ET.SubElement(testPlan, "stringProp", name="TestPlan.user_define_classpath")

    return jmx


def _createThreadGroup(jmx):
    hash = getHashTree(jmx)

    threadGroup = ET.SubElement(
        hash,
        "ThreadGroup",
        guiclass="ThreadGroupGui",
        testclass="ThreadGroup",
        testname="Test Thread Group",
        enabled="true",
    )
    Prop6 = ET.SubElement(threadGroup, "stringProp", name="ThreadGroup.on_sample_error")
    Prop6.text = "continue"
    loopController = ET.SubElement(
        threadGroup,
        "elementProp",
        name="ThreadGroup.main_controller",
        elementType="LoopController",
        guiclass="LoopControlPanel",
        testclass="LoopController",
        testname="Loop Controller",
        enabled="true",
    )
    boolProp1 = ET.SubElement(
        loopController, "boolProp", name="LoopController.continue_forever"
    )
    boolProp1.text = "false"
    stringProp7 = ET.SubElement(
        loopController, "stringProp", name="LoopController.loops"
    )
    stringProp7.text = "1"
    stringProp8 = ET.SubElement(
        threadGroup, "stringProp", name="ThreadGroup.num_threads"
    )
    stringProp8.text = "10"
    stringProp9 = ET.SubElement(threadGroup, "stringProp", name="ThreadGroup.ramp_time")
    stringProp9.text = "10"
    boolProp2 = ET.SubElement(threadGroup, "boolProp", name="ThreadGroup.scheduler")
    boolProp2.text = "false"
    stringProp10 = ET.SubElement(threadGroup, "stringProp", name="ThreadGroup.duration")
    stringProp10.text = ""
    stringProp11 = ET.SubElement(threadGroup, "stringProp", name="ThreadGroup.delay")
    stringProp11.text = ""
    boolProp3 = ET.SubElement(
        threadGroup, "boolProp", name="ThreadGroup.same_user_on_next_iteration"
    )
    boolProp3.text = "true"
    return


def _createHTTPSampler(jmx, hasCounter):
    hash = getHashTree(jmx)

    # Create the HTTPSamplerProxy element
    httpSamplerProxy = ET.SubElement(
        hash,
        "HTTPSamplerProxy",
        guiclass="HttpTestSampleGui",
        testclass="HTTPSamplerProxy",
        testname="HTTP Request",
        enabled="true",
    )

    # Add child elements to the HTTPSamplerProxy element
    elementProp = ET.SubElement(
        httpSamplerProxy,
        "elementProp",
        name="HTTPsampler.Arguments",
        elementType="Arguments",
        guiclass="HTTPArgumentsPanel",
        testclass="Arguments",
        testname="User Defined Variables",
        enabled="true",
    )
    collectionProp = ET.SubElement(
        elementProp, "collectionProp", name="Arguments.arguments"
    )
    stringProp1 = ET.SubElement(
        httpSamplerProxy, "stringProp", name="HTTPSampler.domain"
    )
    stringProp1.text = "${__P(domain)}"
    stringProp2 = ET.SubElement(httpSamplerProxy, "stringProp", name="HTTPSampler.port")
    stringProp2.text = "${__P(port)}"
    stringProp3 = ET.SubElement(
        httpSamplerProxy, "stringProp", name="HTTPSampler.protocol"
    )
    stringProp3.text = "http"
    stringProp4 = ET.SubElement(
        httpSamplerProxy, "stringProp", name="HTTPSampler.contentEncoding"
    )
    stringProp5 = ET.SubElement(httpSamplerProxy, "stringProp", name="HTTPSampler.path")
    stringProp5.text = "${__P(path)}"
    if hasCounter:
        stringProp5.text += "?serial=${serial_counter}"
        pass
    stringProp6 = ET.SubElement(
        httpSamplerProxy, "stringProp", name="HTTPSampler.method"
    )
    stringProp6.text = "GET"
    boolProp1 = ET.SubElement(
        httpSamplerProxy, "boolProp", name="HTTPSampler.follow_redirects"
    )
    boolProp1.text = "true"
    boolProp2 = ET.SubElement(
        httpSamplerProxy, "boolProp", name="HTTPSampler.auto_redirects"
    )
    boolProp2.text = "false"
    boolProp3 = ET.SubElement(
        httpSamplerProxy, "boolProp", name="HTTPSampler.use_keepalive"
    )
    boolProp3.text = "true"
    boolProp4 = ET.SubElement(
        httpSamplerProxy, "boolProp", name="HTTPSampler.DO_MULTIPART_POST"
    )
    boolProp4.text = "false"
    stringProp7 = ET.SubElement(
        httpSamplerProxy, "stringProp", name="HTTPSampler.embedded_url_re"
    )
    stringProp8 = ET.SubElement(
        httpSamplerProxy, "stringProp", name="HTTPSampler.connect_timeout"
    )
    stringProp9 = ET.SubElement(
        httpSamplerProxy, "stringProp", name="HTTPSampler.response_timeout"
    )
    return


def _createCounterConfig(jmx):
    hash = getHashTree(jmx)

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
    stringProp1 = ET.SubElement(counterConfig, "stringProp", name="CounterConfig.start")
    stringProp1.text = "1"
    stringProp2 = ET.SubElement(counterConfig, "stringProp", name="CounterConfig.end")
    stringProp2.text = "999999999"
    stringProp3 = ET.SubElement(counterConfig, "stringProp", name="CounterConfig.incr")
    stringProp3.text = "1"
    stringProp4 = ET.SubElement(counterConfig, "stringProp", name="CounterConfig.name")
    stringProp4.text = "serial_counter"
    stringProp5 = ET.SubElement(
        counterConfig, "stringProp", name="CounterConfig.format"
    )
    stringProp5.text = "000000000"
    boolProp1 = ET.SubElement(counterConfig, "boolProp", name="CounterConfig.per_user")
    boolProp1.text = "false"
    stringProp6 = ET.SubElement(counterConfig, "stringProp", name="TestPlan.comments")
    return


def _createVariableThroughputTimer(jmx):
    hash = getHashTree(jmx)

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
    for i in range(4):
        collectionProp = ET.SubElement(loadProfile, "collectionProp", name="")
        stringProp1 = ET.SubElement(collectionProp, "stringProp", name="")
        stringProp1.text = "10" if i == 0 else str(i * 10)
        stringProp2 = ET.SubElement(collectionProp, "stringProp", name="")
        stringProp2.text = str(i * 10 + 10)
        stringProp3 = ET.SubElement(collectionProp, "stringProp", name="")
        stringProp3.text = "1"
        pass
    return
