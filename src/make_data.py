import xml.etree.cElementTree as et
import pandas as pd
import time
 
# Parser classes from openxes package
from opyenxes.data_in.XUniversalParser import XUniversalParser
from opyenxes.model.XEvent import XEvent
from opyenxes.model.XTrace import XTrace
from opyenxes.model.XAttributeBoolean import XAttributeBoolean
from opyenxes.model.XAttributeCollection import XAttributeCollection
from opyenxes.model.XAttributeContainer import XAttributeContainer
from opyenxes.model.XAttributeContinuous import XAttributeContinuous
from opyenxes.model.XAttributeDiscrete import XAttributeDiscrete
from opyenxes.model.XAttributeID import XAttributeID
from opyenxes.model.XAttributeList import XAttributeList
from opyenxes.model.XAttributeLiteral import XAttributeLiteral
from opyenxes.model.XAttributeMap import XAttributeMap
from opyenxes.model.XAttributeTimestamp import XAttributeTimestamp

log_fp = 'BPI Challenge 2017.xes.gz'

with open(log_fp) as log_file:
    log = XUniversalParser().parse(log_file)[0]




class XLog2df:
    def __init__(self):
        self.__event_ind = 0
        self.__trace_ind = 0
        self.__event_df_dict = dict()
        self.__trace_df_dict = dict()
        
    def parse_xattribute(self, xattrib):
        is_list = isinstance(xattrib, XAttributeList)
        is_container = isinstance(xattrib, XAttributeContainer)

        if is_list or is_container:
            return None, None, None
        else:
            return xattrib.get_key(), xattrib.get_value(), xattrib.get_extension()

    def parse_xattribute_dict(self, xattribs):
        return {key: self.parse_xattribute(val)[1] for key, val in xattribs.items()}

    def xevents2df(self, events, caseid):
        event_df_dict = dict()

        for event in events:
            assert isinstance(event, XEvent)
            attrib_dict = self.parse_xattribute_dict(event.get_attributes())

            # add caseid
            CASEID = 'caseid'
            attrib_dict[CASEID] = caseid
            event_df_dict[self.__event_ind] = attrib_dict
            self.__event_ind += 1
            
        return event_df_dict
    
    def xtraces2df(self, traces):
        trace_df_dict = dict()
        
        for trace in traces:
            attrib_dict = dict(trace.get_attributes())
            attrib_dict = self.parse_xattribute_dict(attrib_dict)
            trace_df_dict[self.__trace_ind] = attrib_dict
            self.__trace_ind += 1
            
        return trace_df_dict
    
    def xlog2df(self, xlog):

        print("Parsing of the file Started...................\n")
        start = time.time()

        trace_df_dict = self.xtraces2df(xlog)
        event_df_dict = dict()
        
        for trace in xlog:
            caseid = trace.get_attributes()['concept:name'].get_value()
            event_df_dict_i = self.xevents2df(trace, caseid)
            event_df_dict.update(event_df_dict_i)
            
        trace_df = pd.DataFrame.from_dict(trace_df_dict, 'index')
        event_df = pd.DataFrame.from_dict(event_df_dict, 'index')
        
        # prefix trace attributes with "trace:" and event attributes with "event:"
        trace_df.columns = ['trace:{}'.format(val) for val in trace_df.columns]
        event_df_columns = []
        CASEID = 'caseid'
        
        for val in event_df.columns:
            renamed = 'event:{}'.format(val)
            if val != CASEID:
                event_df_columns.append(renamed)
            else:
                event_df_columns.append(val)
        
        event_df.columns = event_df_columns
        
        # merge trace_df and event_df on caseid
        trace_df[CASEID] = trace_df['trace:concept:name']
        
        # key column needs to be string type
        trace_df[CASEID] = trace_df[CASEID].astype(str)
        event_df[CASEID] = event_df[CASEID].astype(str)

        merged_df = pd.merge(trace_df, event_df, on=CASEID)

        merged_df['event:org:resource'] = merged_df['event:org:resource'].astype(str)
        merged_df['caseid'] = merged_df['caseid'].astype(str)
        merged_df['trace:concept:name'] = merged_df['trace:concept:name'].astype(str)

        merged_df["Id"] = merged_df["caseid"].apply(lambda x: x.split("_")[1])

        print("Took %.2f seconds for Parsing XES file......................"%(start - time.time()))
        print("\n..............................................")
        print("Sample Parsed Data..............................")
        print(merged_df.shape)

        return merged_df

converter = XLog2df()

event_row_df = converter.xlog2df(log)

print(event_row_df.Id.tail())
event_row_df.to_csv("log_file.csv")
