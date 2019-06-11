#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


# command line arguments
# --report_url=<string>
# --report_file=<string, local file path>
# --commit_hash=<string, full git commit hash>

import argparse
import mysql.connector
import xml.etree.ElementTree as ET

def parse_arguments():
    parser = argparse.ArgumentParser(description="ONNXRuntime test coverge report uploader for dashboard")
    parser.add_argument("--report_url", help="URL to the Cobertura XML report")
    parser.add_argument("--report_file", help="Path to the local cobertura XML report")
    parser.add_argument("--commit_hash", help="Full Git commit hash")
    return parser.parse_args()

def parse_xml_report(report_file):
    tree = ET.parse(report_file) # may throw exception
    root = tree.getroot()
    result = {}
    
    result['coverage'] = float(root.get('line-rate'))
    result['lines_covered'] = int(root.get('lines-covered'))
    result['lines_valid'] = int(root.get('lines-valid'))
    return result

def write_to_db(coverage_data, args):
    # connect to database
    cnx = mysql.connector.connect(
        user='ort@onnxruntimedashboard', 
        password='U5nNR7\e=UPk#Yp!', 
        host='onnxruntimedashboard.mysql.database.azure.com', 
        database='onnxruntime')

    try:
        cursor = cnx.cursor()

        #delete old records
        delete_query = ('DELETE FROM onnxruntime.test_coverage '
            'WHERE UploadTime < DATE_SUB(Now(), INTERVAL 30 DAY);'
        )
        
        cursor.execute(delete_query)

        #insert current record
        insert_query = ('INSERT INTO onnxruntime.test_coverage '
            '(UploadTime, CommitId, Coverage, LinesCovered, TotalLines, ReportURL) '
            'VALUES (Now(), "%s", %f, %d, %d, "%s");'
        )
        
        insert_query = insert_query % (args.commit_hash, 
                                    coverage_data['coverage'], 
                                    coverage_data['lines_covered'],  
                                    coverage_data['lines_valid'],
                                    args.report_url
                                    )

        cursor.execute(insert_query) 
        cnx.close()
    except BaseException as e:
        cnx.close()
        raise e


if __name__ == "__main__":
    try:
        args = parse_arguments()
        coverage_data = parse_xml_report(args.report_file)
        write_to_db(coverage_data, args)
    except BaseException as e:
        print(str(e))
        sys.exit(1)



