import os
import re

from logging_new import setup_logger

def locate_absolute_paths(directory):
    absolute_paths = []
    for root, dirs, files in os.walk(directory):
        logger.info(f"Processing directory: {root} with {dirs} and {files}")
        for file in files:
            logger.info(f"Processing file: {file}")
            file_path = os.path.join(root, file)
            logger.info(f"File path: {file_path}")
            try:
                with open(file_path, 'r') as f:
                    print(f"Processing file: {file_path}")
                    content = f.read()
                    logger.info(f"Content: {content}")
                    matches = re.finditer(r'/Users/[^"\'\s]*', content)
                    logger.info(f"Matches: {matches}")
                    for match in matches:
                        logger.info(f"Match: {match}")
                        line_number = content[:match.start()].count('\n') + 1
                        logger.info(f"Line number: {line_number}")
                        absolute_paths.append(f"{file_path}:{line_number}: {match.group()}")
                        logger.info(f"Absolute path: {absolute_paths}")
            except Exception as e:
                print(f"Error processing file: {file_path}")
                print(f"Error message: {str(e)}")
        logger.info(f"Absolute paths: {absolute_paths}")
    return absolute_paths

logger = setup_logger(__name__)
absolute_paths = locate_absolute_paths('../rjaswal_gpt')
logger.info(f"Absolute paths: {absolute_paths}")

if absolute_paths:
    for path in absolute_paths:
        print(path)
else:
    print("No absolute paths found in the codebase.")