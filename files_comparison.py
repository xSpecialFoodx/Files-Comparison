import string
import math
import sys
import os
import argparse
import distutils.dir_util

#
# #
# # #
# # # # files comparison
# # #
# #
#


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.stderr.write('\nerror: {0}\n'.format(message))
        sys.exit(2)


def CheckHexText(source, length, add_0x):  # returns the hex text
    source_hex = str(hex(source)[2:])
    source_hex_length = len(source_hex)
    source_hex_index = None
    source_hex_cell = None

    for source_hex_index in range(0, source_hex_length):
        source_hex_cell = source_hex[source_hex_index]

        if (source_hex_cell in string.hexdigits) is False:
            source_hex = source_hex[:source_hex_index]

            break

    result = str(source_hex.zfill(length))

    if add_0x is True:
        result = "0x" + result

    return result


def FastCheckHexText(source, length):  # returns the hex text
    source_hex = str(hex(source)[2:])

    result = str(source_hex.zfill(length))

    return result


def add_comparison(
    first_file_data_location
    , first_file_data_byte
    , second_file_data_location
    , second_file_data_byte
    , show_comparison
    , comparison_type  # 0 - match, otherwise - difference
):
    result = []

    first_file_data_byte_fixed = None
    first_file_data_byte_size = 0
    second_file_data_byte_fixed = None
    second_file_data_byte_size = 0

    if first_file_data_byte is not None:
        first_file_data_byte_size = 1

        if show_comparison is True:
            first_file_data_byte_fixed = FastCheckHexText(first_file_data_byte, 2)

    if second_file_data_byte is not None:
        second_file_data_byte_size = 1

        if show_comparison is True:
            if comparison_type != 0:
                second_file_data_byte_fixed = FastCheckHexText(second_file_data_byte, 2)

    result.append(first_file_data_location)
    result.append(first_file_data_byte_fixed)
    result.append(first_file_data_byte_size)
    result.append(second_file_data_location)
    result.append(second_file_data_byte_fixed)
    result.append(second_file_data_byte_size)

    return result


def combine_comparisons(
    comparisons
    , comparison_type  # 0 - match, otherwise - difference
):
    result = None

    current_result = None

    comparisons_amount = len(comparisons)

    if comparisons_amount > 0:
        comparisons_index = None
        comparison = comparisons[0]
        comparison_first_file_data_location = comparison[0]
        comparison_first_file_data_byte_fixed = comparison[1]
        comparison_first_file_data_byte_fixed_size = comparison[2]
        comparison_second_file_data_location = comparison[3]
        comparison_second_file_data_byte_fixed = comparison[4]
        comparison_second_file_data_byte_fixed_size = comparison[5]

        current_result = []
        current_result_amount = 0
        current_result_cell = comparison.copy()
        current_result_cell_first_file_data_location = current_result_cell[0]
        current_result_cell_first_file_data_bytes = []

        if current_result_cell[1] is not None:
            current_result_cell_first_file_data_bytes.append(current_result_cell[1])

        current_result_cell[1] = current_result_cell_first_file_data_bytes

        current_result_cell_first_file_data_bytes_size = current_result_cell[2]
        current_result_cell_second_file_data_location = current_result_cell[3]

        if comparison_type != 0:
            current_result_cell_second_file_data_bytes = []

            if current_result_cell[4] is not None:
                current_result_cell_second_file_data_bytes.append(current_result_cell[4])
        else:
            current_result_cell_second_file_data_bytes = None

        current_result_cell[4] = current_result_cell_second_file_data_bytes

        current_result_cell_second_file_data_bytes_size = current_result_cell[5]

        current_result.append(current_result_cell)

        current_result_amount += 1

        for comparisons_index in range(1, comparisons_amount):
            comparison = comparisons[comparisons_index]
            comparison_first_file_data_location = comparison[0]
            comparison_first_file_data_byte_fixed = comparison[1]
            comparison_first_file_data_byte_fixed_size = comparison[2]
            comparison_second_file_data_location = comparison[3]
            comparison_second_file_data_byte_fixed = comparison[4]
            comparison_second_file_data_byte_fixed_size = comparison[5]

            if (
                current_result_cell_first_file_data_location + current_result_cell_first_file_data_bytes_size >= comparison_first_file_data_location
                and current_result_cell_second_file_data_location + current_result_cell_second_file_data_bytes_size >= comparison_second_file_data_location
            ):
                if current_result_cell_first_file_data_location + current_result_cell_first_file_data_bytes_size == comparison_first_file_data_location:
                    if comparison_first_file_data_location > current_result_cell_first_file_data_location:
                        if comparison_first_file_data_byte_fixed is not None:
                            current_result_cell_first_file_data_bytes.append(comparison_first_file_data_byte_fixed)

                        current_result_cell[1] = current_result_cell_first_file_data_bytes  # not necessary, but just for the record

                        current_result_cell_first_file_data_bytes_size += comparison_first_file_data_byte_fixed_size

                        current_result_cell[2] = current_result_cell_first_file_data_bytes_size

                if current_result_cell_second_file_data_location + current_result_cell_second_file_data_bytes_size == comparison_second_file_data_location:
                    if comparison_second_file_data_location > current_result_cell_second_file_data_location:
                        if comparison_type != 0:
                            if comparison_second_file_data_byte_fixed is not None:
                                current_result_cell_second_file_data_bytes.append(comparison_second_file_data_byte_fixed)

                            current_result_cell[4] = current_result_cell_second_file_data_bytes  # not necessary, but just for the record

                        current_result_cell_second_file_data_bytes_size += comparison_second_file_data_byte_fixed_size

                        current_result_cell[5] = current_result_cell_second_file_data_bytes_size
            else:
                current_result_cell = comparison.copy()
                current_result_cell_first_file_data_location = current_result_cell[0]
                current_result_cell_first_file_data_bytes = []

                if current_result_cell[1] is not None:
                    current_result_cell_first_file_data_bytes.append(current_result_cell[1])

                current_result_cell[1] = current_result_cell_first_file_data_bytes

                current_result_cell_first_file_data_bytes_size = current_result_cell[2]
                current_result_cell_second_file_data_location = current_result_cell[3]

                if comparison_type != 0:
                    current_result_cell_second_file_data_bytes = []

                    if current_result_cell[4] is not None:
                        current_result_cell_second_file_data_bytes.append(current_result_cell[4])
                else:
                    current_result_cell_second_file_data_bytes = None

                current_result_cell[4] = current_result_cell_second_file_data_bytes

                current_result_cell_second_file_data_bytes_size = current_result_cell[5]

                current_result.append(current_result_cell)

                current_result_amount += 1

    result = current_result

    return result


Debug = False

parser = MyParser(description='files comparison tool')

if Debug is False:
    parser.add_argument('--first', required=False, type=str, help='first file')
    parser.add_argument('--second', required=False, type=str, help='second file')
    parser.add_argument('--output', required=False, default="", type=str, help='new file')
    parser.add_argument('--dry-run', required=False, default=False, action='store_true', help='if inserted then nothing will be written to the output file')
    parser.add_argument('--verbose', required=False, default=False, action='store_true', help='detailed printing')
    parser.add_argument('--files-comparison-type', required=False, default="0", type=str, help='0 - absolute files comparison, otherwise - relative files comparison')
    parser.add_argument('--show-matches', required=False, default=False, action='store_true', help='if enabled then showing the matches and/or writing them in the output text file')
    parser.add_argument('--hide-differences', required=False, default=False, action='store_true', help='if enabled then hiding the differences and/or not writing them in the output text file')
    parser.add_argument('--first-file-data-start-location', required=False, default="0", type=str, help='the location to start comparing in the first file')
    parser.add_argument('--first-file-data-end-location', required=False, default="0", type=str, help='the location to end comparing in the first file, set as 0 for the first file size - 1')
    parser.add_argument('--second-file-data-start-location', required=False, default="0", type=str, help='the location to start comparing in the second file')
    parser.add_argument('--second-file-data-end-location', required=False, default="0", type=str, help='the location to end comparing in the second file, set as 0 for the second file size - 1')
    parser.add_argument('--files-data-offsets-max-absolute-differences', required=False, default=str(int(math.pow(2, 3))), type=str, help='relevant only to relative files comparison - bytes to differenciate at most forward (not including the original difference), set as a negative number for infinite')
    parser.add_argument('--files-data-offsets-min-absolute-matches', required=False, default=str(int(math.pow(2, 2))), type=str, help='relevant only to relative files comparison - bytes to match at least forward (not including the original match)')
    parser.add_argument('--files-data-offsets-max-relative-differences', required=False, default=str(int(math.pow(2, 10))), type=str, help='relevant only to relative files comparison - bytes to differenciate at most forward (not including the original difference), set as a negative number for infinite')
    parser.add_argument('--files-data-offsets-min-relative-matches', required=False, default=str(int(math.pow(2, 5))), type=str, help='relevant only to relative files comparison - bytes to match at least forward (not including the original match)')
    parser.add_argument('--files-data-offsets-min-resolution-difference-gain', required=False, default=str(int(math.pow(2, 0))), type=str, help='relevant only to relative files comparison - min resolution gain between comparisons')
    parser.add_argument('--files-data-offsets-max-resolution-difference-gain', required=False, default=str(int(math.pow(2, 5))), type=str, help='relevant only to relative files comparison - max resolution gain between comparisons, set as 0 for infinite')
    parser.add_argument('--files-data-offsets-max-resolution-difference-percentage-gain', required=False, default="50", type=str, help='relevant only to relative files comparison - max resolution percentage gain between comparisons (from the current resolution)')

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit(1)
else:
    parser.add_argument('--first', required=False, default="C:/somefolder/somefileA.bin", type=str, help='first file')
    parser.add_argument('--second', required=False, default="C:/somefolder/somefileB.bin", type=str, help='second file')
    parser.add_argument('--output', required=False, default="", type=str, help='new file')
    parser.add_argument('--dry-run', required=False, default=False, action='store_true', help='if inserted then nothing will be written to the output file')
    parser.add_argument('--verbose', required=False, default=False, action='store_true', help='detailed printing')
    parser.add_argument('--files-comparison-type', required=False, default="0", type=str, help='0 - absolute files comparison, otherwise - relative files comparison')
    parser.add_argument('--show-matches', required=False, default=False, action='store_true', help='if enabled then showing the matches and/or writing them in the output text file')
    parser.add_argument('--hide-differences', required=False, default=False, action='store_true', help='if enabled then hiding the differences and/or not writing them in the output text file')
    parser.add_argument('--first-file-data-start-location', required=False, default="0", type=str, help='the location to start comparing in the first file')
    parser.add_argument('--first-file-data-end-location', required=False, default="0", type=str, help='the location to end comparing in the first file, set as 0 for the first file size - 1')
    parser.add_argument('--second-file-data-start-location', required=False, default="0", type=str, help='the location to start comparing in the first file')
    parser.add_argument('--second-file-data-end-location', required=False, default="0", type=str, help='the location to end comparing in the second file, set as 0 for the second file size - 1')
    parser.add_argument('--files-data-offsets-max-absolute-differences', required=False, default=str(int(math.pow(2, 3))), type=str, help='relevant only to relative files comparison - bytes to differenciate at most forward (not including the original difference), set as a negative number for infinite')
    parser.add_argument('--files-data-offsets-min-absolute-matches', required=False, default=str(int(math.pow(2, 2))), type=str, help='relevant only to relative files comparison - bytes to match at least forward (not including the original match)')
    parser.add_argument('--files-data-offsets-max-relative-differences', required=False, default=str(int(math.pow(2, 10))), type=str, help='relevant only to relative files comparison - bytes to differenciate at most forward (not including the original difference), set as a negative number for infinite')
    parser.add_argument('--files-data-offsets-min-relative-matches', required=False, default=str(int(math.pow(2, 5))), type=str, help='relevant only to relative files comparison - bytes to match at least forward (not including the original match)')
    parser.add_argument('--files-data-offsets-min-resolution-difference-gain', required=False, default=str(int(math.pow(2, 0))), type=str, help='relevant only to relative files comparison - min resolution gain between comparisons')
    parser.add_argument('--files-data-offsets-max-resolution-difference-gain', required=False, default=str(int(math.pow(2, 5))), type=str, help='relevant only to relative files comparison - max resolution gain between comparisons, set as 0 for infinite')
    parser.add_argument('--files-data-offsets-max-resolution-difference-percentage-gain', required=False, default="50", type=str, help='relevant only to relative files comparison - max resolution percentage gain between comparisons (from the current resolution)')

args = parser.parse_args()


def main():
    global parser

    global args

    Headers = None
    Fields = None
    Field = None

    AddressesLength = 8  # 16
    SizeLength = 8  # 16

    first_file_path = os.path.abspath(args.first).replace('\\', '/')

    if not os.path.isfile(first_file_path):
        parser.error('invalid first file: {0}'.format(first_file_path))

    first_file_size = os.path.getsize(first_file_path)

    second_file_path = os.path.abspath(args.second).replace('\\', '/')

    if not os.path.isfile(second_file_path):
        parser.error('invalid second file: {0}'.format(second_file_path))

    second_file_size = os.path.getsize(second_file_path)

    if args.output == "":
        first_file_name = os.path.basename(first_file_path)
        first_file_name_length = len(first_file_name)
        first_file_name_splitted = first_file_name.split(".")
        first_file_name_splitted_amount = len(first_file_name_splitted)
        first_file_name_extension = first_file_name_splitted[first_file_name_splitted_amount - 1]
        first_file_name_extension_length = len(first_file_name_extension)
        first_file_name_without_extension = first_file_name[:first_file_name_length - first_file_name_extension_length - 1]

        second_file_name = os.path.basename(second_file_path)
        second_file_name_length = len(second_file_name)
        second_file_name_splitted = second_file_name.split(".")
        second_file_name_splitted_amount = len(second_file_name_splitted)
        second_file_name_extension = second_file_name_splitted[second_file_name_splitted_amount - 1]
        second_file_name_extension_length = len(second_file_name_extension)
        second_file_name_without_extension = second_file_name[:second_file_name_length - second_file_name_extension_length - 1]

        output_file_name_extension = "txt"
        output_file_name_without_extension = first_file_name_without_extension + '-' + second_file_name_without_extension + '-' + "comparison_result"

        output_file_name = output_file_name_without_extension + '.' + output_file_name_extension

        output_file_path = os.path.abspath(output_file_name).replace('\\', '/')
    else:
        output_file_path = os.path.abspath(args.output).replace('\\', '/')

    output_folder_path = os.path.dirname(output_file_path).replace('\\', '/')

    if output_folder_path[len(output_folder_path) - 1] == '/':
        output_folder_path = output_folder_path[:-1]

    if args.dry_run is False:
        distutils.dir_util.mkpath(output_folder_path)

    if os.path.exists(output_file_path) and not os.path.isfile(output_file_path):
        parser.error('invalid output file: {0}'.format(output_file_path))

    files_comparison_type = (1 if args.files_comparison_type != "0" else 0)  # 1

    show_matches = (args.show_matches is True)
    show_differences = (args.hide_differences is False)

    first_file_data_start_location = int(args.first_file_data_start_location)
    first_file_data_end_location = int(args.first_file_data_end_location)

    second_file_data_start_location = int(args.second_file_data_start_location)
    second_file_data_end_location = int(args.second_file_data_end_location)

    if first_file_data_end_location == 0:
        first_file_data_end_location = first_file_size - 1

    if first_file_data_start_location > first_file_data_end_location:
        first_file_data_start_location = first_file_data_end_location

    if second_file_data_end_location == 0:
        second_file_data_end_location = second_file_size - 1

    if second_file_data_start_location > second_file_data_end_location:
        second_file_data_start_location = second_file_data_end_location

    print(
        "First File:" + ' ' + first_file_path + "\n"
        + "Second File:" + ' ' + second_file_path + "\n"
        + "Output:" + ' ' + output_file_path + "\n"
        + "Dry Run:" + ' ' + ("True" if args.dry_run is True else "False") + "\n"
        + "Verbose:" + ' ' + ("True" if args.verbose is True else "False") + "\n"
        + "Files Comparison Type:" + ' ' + ("Relative" if args.files_comparison_type != "0" else "Absolute") + "\n"
        + "Show Matches:" + ' ' + ("True" if args.show_matches is True else "False") + "\n"
        + "Show Differences:" + ' ' + ("True" if args.hide_differences is False else "False") + "\n"
        + "First File Data Start Location:" + ' ' + str(CheckHexText(first_file_data_start_location, AddressesLength, True)) + "\n"
        + "First File Data End Location:" + ' ' + str(CheckHexText(first_file_data_end_location, AddressesLength, True)) + "\n"
        + "Second File Data Start Location:" + ' ' + str(CheckHexText(second_file_data_start_location, AddressesLength, True)) + "\n"
        + "Second File Data End Location:" + ' ' + str(CheckHexText(second_file_data_end_location, AddressesLength, True)) + "\n"
        + "Files Data Offsets Max Absolute Differences:" + ' ' + args.files_data_offsets_max_absolute_differences + "\n"
        + "Files Data Offsets Min Absolute Matches:" + ' ' + args.files_data_offsets_min_absolute_matches + "\n"
        + "Files Data Offsets Max Relative Differences:" + ' ' + args.files_data_offsets_max_relative_differences + "\n"
        + "Files Data Offsets Min Relative Matches:" + ' ' + args.files_data_offsets_min_relative_matches + "\n"
        + "Files Data Offsets Min Resolution Difference Gain:" + ' ' + args.files_data_offsets_min_resolution_difference_gain + "\n"
        + "Files Data Offsets Max Resolution Difference Gain:" + ' ' + args.files_data_offsets_max_resolution_difference_gain + "\n"
        + "Files Data Offsets Max Resolution Difference Percentage Gain:" + ' ' + args.files_data_offsets_max_resolution_difference_percentage_gain + '%'
    )

    print("")
    print('processing comparison result file: {0}'.format(output_file_path))

    files_data_offsets_max_absolute_differences = int(args.files_data_offsets_max_absolute_differences)  # 0
    files_data_offsets_min_absolute_matches = int(args.files_data_offsets_min_absolute_matches)  # 0
    files_data_offsets_min_absolute_matches_index = None

    files_data_offsets_max_relative_differences = int(args.files_data_offsets_max_relative_differences)  # 0
    files_data_offsets_min_relative_matches = int(args.files_data_offsets_min_relative_matches)  # 0
    files_data_offsets_min_relative_matches_index = None

    files_data_offsets_min_resolution_difference_gain = int(args.files_data_offsets_min_resolution_difference_gain)
    files_data_offsets_max_resolution_difference_gain = int(args.files_data_offsets_max_resolution_difference_gain)
    files_data_offsets_max_resolution_difference_percentage_gain = int(args.files_data_offsets_max_resolution_difference_percentage_gain)
    files_data_offsets_current_resolution = None
    files_data_offsets_last_resolution = None

    files_data_offsets_backward_matches_index = None
    files_data_offsets_backward_matches_min_possible_index = None

    first_file_data = None
    first_file_data_size = None
    first_file_data_min_location = None
    first_file_data_min_possible_location = None
    first_file_data_max_location = None
    first_file_data_max_possible_location = None
    first_file_data_location = first_file_data_start_location
    first_file_data_location_index = None
    first_file_data_min_offset = None
    first_file_data_min_possible_offset = None
    first_file_data_max_offset = None
    first_file_data_max_possible_offset = None
    first_file_data_offset = None
    first_file_data_offset_index = None
    first_file_data_cell = None

    second_file_data = None
    second_file_data_size = None
    second_file_data_min_location = None
    second_file_data_min_possible_location = None
    second_file_data_max_location = None
    second_file_data_max_possible_location = None
    second_file_data_location = second_file_data_start_location
    second_file_data_location_index = None
    second_file_data_min_offset = None
    second_file_data_min_possible_offset = None
    second_file_data_max_offset = None
    second_file_data_max_possible_offset = None
    second_file_data_offset = None
    second_file_data_offset_index = None
    second_file_data_cell = None

    output_file_data_list = None
    output_file_data_list_cell = None
    output_file_data = None

    matches = []
    matches_amount = 0
    match = None

    matches_sequences = None
    matches_sequences_amount = 0

    differences = []
    differences_amount = 0
    difference = None

    differences_sequences = None
    differences_sequences_amount = 0

    buffer_size = int(math.pow(2, 18))  # 256 KB  # 10

    # smaller_file_size = first_file_size if first_file_size < second_file_size else second_file_size
    # bigger_file_size = first_file_size if first_file_size > second_file_size else second_file_size

    method_found = False
    error_found = False

    with open(first_file_path, 'rb') as ff:
        with open(second_file_path, 'rb') as sf:
            if first_file_data_location > 0:
                ff.seek(first_file_data_location, os.SEEK_CUR)

            if second_file_data_location > 0:
                sf.seek(second_file_data_location, os.SEEK_CUR)

            print("")
            print('comparing files')

            while (
                first_file_data_location <= first_file_data_end_location
                or second_file_data_location <= second_file_data_end_location
            ):
                if first_file_data_location > first_file_data_end_location:
                    first_file_data = None
                    first_file_data_size = 0
                else:
                    if first_file_data_location + buffer_size - 1 > first_file_data_end_location:
                        first_file_data_size = first_file_data_end_location - first_file_data_location + 1
                    else:
                        first_file_data_size = buffer_size

                    first_file_data = ff.read(first_file_data_size)

                if second_file_data_location > second_file_data_end_location:
                    second_file_data = None
                    second_file_data_size = 0
                else:
                    if second_file_data_location + buffer_size - 1 > second_file_data_end_location:
                        second_file_data_size = second_file_data_end_location - second_file_data_location + 1
                    else:
                        second_file_data_size = buffer_size

                    second_file_data = sf.read(second_file_data_size)

                first_file_data_offset = 0

                if 0 < first_file_data_size:
                    first_file_data_cell = first_file_data[0]
                else:
                    first_file_data_cell = None

                second_file_data_offset = 0

                if 0 < second_file_data_size:
                    second_file_data_cell = second_file_data[0]
                else:
                    second_file_data_cell = None

                while (
                    (  # end of either files
                        first_file_data_size != buffer_size
                        or second_file_data_size != buffer_size
                    )
                    and
                    (  # either offsets cells are not None
                        first_file_data_offset < first_file_data_size
                        or second_file_data_offset < second_file_data_size
                    )
                    or
                    (  # both offsets cells are not None
                        first_file_data_offset < first_file_data_size
                        and second_file_data_offset < second_file_data_size
                    )
                ):
                    # checking if the first file data cell and the second file data cell match, if so set method found as True

                    if (
                        first_file_data_cell is not None
                        and second_file_data_cell is not None
                    ):
                        if first_file_data_cell == second_file_data_cell:
                            method_found = True

                            match = (
                                add_comparison(
                                    first_file_data_location
                                    , first_file_data_cell
                                    , second_file_data_location
                                    , second_file_data_cell
                                    , show_matches
                                    , 0
                                )
                            )

                            matches.append(match)

                            matches_amount += 1

                    # otherwise if method found isn't True from here forward then need to add the difference/s

                    if method_found is False:
                        if (  # if at the end of either files so enter anyway, since it's a difference and no further matches can be found
                            files_comparison_type == 0
                            or first_file_data_cell is None
                            or second_file_data_cell is None
                        ):
                            method_found = True

                            difference = (
                                add_comparison(
                                    first_file_data_location
                                    , first_file_data_cell
                                    , second_file_data_location
                                    , second_file_data_cell
                                    , show_differences
                                    , 1
                                )
                            )

                            differences.append(difference)

                            differences_amount += 1

                    # if method found is still False by here then do a relative files comparison

                    if method_found is False:
                        files_data_offsets_current_resolution = files_data_offsets_min_resolution_difference_gain
                        files_data_offsets_last_resolution = files_data_offsets_current_resolution

                        files_data_offsets_backward_matches_min_possible_index = 0

                        first_file_data_min_location = first_file_data_location
                        first_file_data_min_possible_location = -1
                        first_file_data_min_offset = first_file_data_offset
                        first_file_data_min_possible_offset = -1

                        second_file_data_min_location = second_file_data_location
                        second_file_data_min_possible_location = -1
                        second_file_data_min_offset = second_file_data_offset
                        second_file_data_min_possible_offset = -1

                        # checking for the max possible locations and offsets

                        if (
                            files_data_offsets_max_absolute_differences >= 0
                            or files_data_offsets_max_relative_differences >= 0
                        ):
                            if (
                                files_data_offsets_max_absolute_differences >= 0
                                and files_data_offsets_max_absolute_differences > files_data_offsets_max_relative_differences
                            ):
                                first_file_data_max_possible_location = first_file_data_min_location + files_data_offsets_max_absolute_differences
                            else:
                                first_file_data_max_possible_location = first_file_data_min_location + files_data_offsets_max_relative_differences

                            if first_file_data_max_possible_location >= first_file_data_min_location + (first_file_data_size - first_file_data_min_offset):
                                first_file_data_max_possible_location = first_file_data_min_location + (first_file_data_size - first_file_data_min_offset) - 1
                        else:
                            first_file_data_max_possible_location = first_file_data_min_location + (first_file_data_size - first_file_data_min_offset) - 1

                        if (
                            files_data_offsets_max_absolute_differences >= 0
                            or files_data_offsets_max_relative_differences >= 0
                        ):
                            if (
                                files_data_offsets_max_absolute_differences >= 0
                                and files_data_offsets_max_absolute_differences > files_data_offsets_max_relative_differences
                            ):
                                first_file_data_max_possible_offset = first_file_data_min_offset + files_data_offsets_max_absolute_differences
                            else:
                                first_file_data_max_possible_offset = first_file_data_min_offset + files_data_offsets_max_relative_differences

                            if first_file_data_max_possible_offset >= first_file_data_size:
                                first_file_data_max_possible_offset = first_file_data_size - 1
                        else:
                            first_file_data_max_possible_offset = first_file_data_size - 1

                        if (
                            files_data_offsets_max_absolute_differences >= 0
                            or files_data_offsets_max_relative_differences >= 0
                        ):
                            if (
                                files_data_offsets_max_absolute_differences >= 0
                                and files_data_offsets_max_absolute_differences > files_data_offsets_max_relative_differences
                            ):
                                second_file_data_max_possible_location = second_file_data_min_location + files_data_offsets_max_absolute_differences
                            else:
                                second_file_data_max_possible_location = second_file_data_min_location + files_data_offsets_max_relative_differences

                            if second_file_data_max_possible_location >= second_file_data_min_location + (second_file_data_size - second_file_data_min_offset):
                                second_file_data_max_possible_location = second_file_data_min_location + (second_file_data_size - second_file_data_min_offset) - 1
                        else:
                            second_file_data_max_possible_location = second_file_data_min_location + (second_file_data_size - second_file_data_min_offset) - 1

                        if (
                            files_data_offsets_max_absolute_differences >= 0
                            or files_data_offsets_max_relative_differences >= 0
                        ):
                            if (
                                files_data_offsets_max_absolute_differences >= 0
                                and files_data_offsets_max_absolute_differences > files_data_offsets_max_relative_differences
                            ):
                                second_file_data_max_possible_offset = second_file_data_min_offset + files_data_offsets_max_absolute_differences
                            else:
                                second_file_data_max_possible_offset = second_file_data_min_offset + files_data_offsets_max_relative_differences

                            if second_file_data_max_possible_offset >= second_file_data_size:
                                second_file_data_max_possible_offset = second_file_data_size - 1
                        else:
                            second_file_data_max_possible_offset = second_file_data_size - 1

                        # do an absolute files comparison

                        if files_data_offsets_max_absolute_differences >= 0:
                            first_file_data_max_location = first_file_data_min_location + files_data_offsets_max_absolute_differences

                            if first_file_data_max_location >= first_file_data_min_location + (first_file_data_size - first_file_data_min_offset):
                                first_file_data_max_location = first_file_data_min_location + (first_file_data_size - first_file_data_min_offset) - 1
                        else:
                            first_file_data_max_location = first_file_data_min_location + (first_file_data_size - first_file_data_min_offset) - 1

                        if files_data_offsets_max_absolute_differences >= 0:
                            first_file_data_max_offset = first_file_data_min_offset + files_data_offsets_max_absolute_differences

                            if first_file_data_max_offset >= first_file_data_size:
                                first_file_data_max_offset = first_file_data_size - 1
                        else:
                            first_file_data_max_offset = first_file_data_size - 1

                        if files_data_offsets_max_absolute_differences >= 0:
                            second_file_data_max_location = second_file_data_min_location + files_data_offsets_max_absolute_differences

                            if second_file_data_max_location >= second_file_data_min_location + (second_file_data_size - second_file_data_min_offset):
                                second_file_data_max_location = second_file_data_min_location + (second_file_data_size - second_file_data_min_offset) - 1
                        else:
                            second_file_data_max_location = second_file_data_min_location + (second_file_data_size - second_file_data_min_offset) - 1

                        if files_data_offsets_max_absolute_differences >= 0:
                            second_file_data_max_offset = second_file_data_min_offset + files_data_offsets_max_absolute_differences

                            if second_file_data_max_offset >= second_file_data_size:
                                second_file_data_max_offset = second_file_data_size - 1
                        else:
                            second_file_data_max_offset = second_file_data_size - 1

                        # already checked the last one

                        first_file_data_location = first_file_data_min_location + 1
                        first_file_data_offset = first_file_data_min_offset + 1

                        if (
                            first_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                            and first_file_data_offset <= first_file_data_max_offset
                        ):
                            first_file_data_cell = first_file_data[first_file_data_offset]
                        else:
                            first_file_data_cell = None

                        second_file_data_location = second_file_data_min_location + 1
                        second_file_data_offset = second_file_data_min_offset + 1

                        if (
                            second_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                            and second_file_data_offset <= second_file_data_max_offset
                        ):
                            second_file_data_cell = second_file_data[second_file_data_offset]
                        else:
                            second_file_data_cell = None

                        while (
                            first_file_data_offset <= first_file_data_max_offset
                            and second_file_data_offset <= second_file_data_max_offset
                        ):
                            if first_file_data_cell != second_file_data_cell:
                                error_found = True
                            else:
                                # checking the first match location
                                # (no need to actually check because in absolute files comparison the first found match is the first match)

                                files_data_offsets_backward_matches_index = 0

                                if (
                                    first_file_data_min_possible_offset == -1
                                    or (
                                        first_file_data_offset - files_data_offsets_backward_matches_index < first_file_data_min_possible_offset
                                        or (
                                            first_file_data_offset - files_data_offsets_backward_matches_index == first_file_data_min_possible_offset
                                            and (
                                                second_file_data_min_possible_offset == -1
                                                or (
                                                    second_file_data_offset - files_data_offsets_backward_matches_index < second_file_data_min_possible_offset
                                                )
                                            )
                                        )
                                    )
                                ):
                                    files_data_offsets_backward_matches_min_possible_index = files_data_offsets_backward_matches_index

                                    first_file_data_min_possible_location = first_file_data_location
                                    first_file_data_min_possible_offset = first_file_data_offset

                                    second_file_data_min_possible_location = second_file_data_location
                                    second_file_data_min_possible_offset = second_file_data_offset

                                # checking forward matches after the first match

                                files_data_offsets_min_absolute_matches_index = 1  # 0 already matches

                                while files_data_offsets_min_absolute_matches_index <= files_data_offsets_min_absolute_matches:
                                    if (
                                        first_file_data_offset
                                        - files_data_offsets_backward_matches_index
                                        + files_data_offsets_min_absolute_matches_index
                                        >= 0  # for sure bigger than 0, but just for reference
                                        and
                                        first_file_data_offset
                                        - files_data_offsets_backward_matches_index
                                        + files_data_offsets_min_absolute_matches_index
                                        <= first_file_data_size - 1
                                    ):
                                        first_file_data_cell = (
                                            first_file_data[
                                                first_file_data_offset
                                                - files_data_offsets_backward_matches_index
                                                + files_data_offsets_min_absolute_matches_index
                                            ]
                                        )
                                    else:
                                        first_file_data_cell = None

                                    if (
                                        second_file_data_offset
                                        - files_data_offsets_backward_matches_index
                                        + files_data_offsets_min_absolute_matches_index
                                        >= 0  # for sure bigger than 0, but just for reference
                                        and
                                        second_file_data_offset
                                        - files_data_offsets_backward_matches_index
                                        + files_data_offsets_min_absolute_matches_index
                                        <= second_file_data_size - 1
                                    ):
                                        second_file_data_cell = (
                                            second_file_data[
                                                second_file_data_offset
                                                - files_data_offsets_backward_matches_index
                                                + files_data_offsets_min_absolute_matches_index
                                            ]
                                        )
                                    else:
                                        second_file_data_cell = None

                                    if (
                                        first_file_data_cell is None
                                        and second_file_data_cell is None
                                    ):
                                        break
                                    else:
                                        if (
                                            first_file_data_cell is None
                                            or second_file_data_cell is None
                                        ):
                                            error_found = True
                                        else:
                                            if first_file_data_cell != second_file_data_cell:
                                                error_found = True

                                    if error_found is True:
                                        break
                                    else:
                                        files_data_offsets_min_absolute_matches_index += 1

                            if error_found is True:
                                error_found = False
                            else:
                                method_found = True

                            if method_found is True:
                                break
                            else:
                                first_file_data_location += 1
                                first_file_data_offset += 1

                                if first_file_data_offset <= first_file_data_max_offset:
                                    first_file_data_cell = first_file_data[first_file_data_offset]
                                else:
                                    first_file_data_cell = None

                                second_file_data_location += 1
                                second_file_data_offset += 1

                                if second_file_data_offset <= second_file_data_max_offset:
                                    second_file_data_cell = second_file_data[second_file_data_offset]
                                else:
                                    second_file_data_cell = None

                        if method_found is True:
                            # going to the first found match because we'll meet the next one later on anyway
                            # (checked for forward matches only in order to validate that the short range is suitable)

                            if (
                                first_file_data_min_possible_location != -1
                                and first_file_data_min_possible_offset != -1
                                and second_file_data_min_possible_location != -1
                                and second_file_data_min_possible_offset != -1
                            ):
                                files_data_offsets_backward_matches_index = files_data_offsets_backward_matches_min_possible_index

                                first_file_data_location = first_file_data_min_possible_location
                                first_file_data_offset = first_file_data_min_possible_offset

                                second_file_data_location = second_file_data_min_possible_location
                                second_file_data_offset = second_file_data_min_possible_offset

                        if method_found is False:
                            # do a relative files comparison

                            if files_data_offsets_max_relative_differences >= 0:
                                first_file_data_max_location = first_file_data_min_location + files_data_offsets_max_relative_differences

                                if first_file_data_max_location >= first_file_data_min_location + (first_file_data_size - first_file_data_min_offset):
                                    first_file_data_max_location = first_file_data_min_location + (first_file_data_size - first_file_data_min_offset) - 1
                            else:
                                first_file_data_max_location = first_file_data_min_location + (first_file_data_size - first_file_data_min_offset) - 1

                            if files_data_offsets_max_relative_differences >= 0:
                                first_file_data_max_offset = first_file_data_min_offset + files_data_offsets_max_relative_differences

                                if first_file_data_max_offset >= first_file_data_size:
                                    first_file_data_max_offset = first_file_data_size - 1
                            else:
                                first_file_data_max_offset = first_file_data_size - 1

                            if files_data_offsets_max_relative_differences >= 0:
                                second_file_data_max_location = second_file_data_min_location + files_data_offsets_max_relative_differences

                                if second_file_data_max_location >= second_file_data_min_location + (second_file_data_size - second_file_data_min_offset):
                                    second_file_data_max_location = second_file_data_min_location + (second_file_data_size - second_file_data_min_offset) - 1
                            else:
                                second_file_data_max_location = second_file_data_min_location + (second_file_data_size - second_file_data_min_offset) - 1

                            if files_data_offsets_max_relative_differences >= 0:
                                second_file_data_max_offset = second_file_data_min_offset + files_data_offsets_max_relative_differences

                                if second_file_data_max_offset >= second_file_data_size:
                                    second_file_data_max_offset = second_file_data_size - 1
                            else:
                                second_file_data_max_offset = second_file_data_size - 1

                            # already checked the last one

                            first_file_data_location = first_file_data_min_location
                            first_file_data_offset = first_file_data_min_offset

                            if (
                                first_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                                and first_file_data_offset <= first_file_data_max_offset
                            ):
                                first_file_data_cell = first_file_data[first_file_data_offset]
                            else:
                                first_file_data_cell = None

                            second_file_data_location = second_file_data_min_location + 1
                            second_file_data_offset = second_file_data_min_offset + 1

                            if (
                                second_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                                and second_file_data_offset <= second_file_data_max_offset
                            ):
                                second_file_data_cell = second_file_data[second_file_data_offset]
                            else:
                                second_file_data_cell = None

                            while (
                                first_file_data_offset <= first_file_data_max_offset
                                and second_file_data_offset <= second_file_data_max_offset
                            ):
                                if first_file_data_cell != second_file_data_cell:
                                    error_found = True
                                else:
                                    # checking the first match location

                                    files_data_offsets_backward_matches_index = 1

                                    while (
                                        first_file_data_offset - files_data_offsets_backward_matches_index >= 0
                                        and first_file_data_offset - files_data_offsets_backward_matches_index >= first_file_data_min_offset
                                        and second_file_data_offset - files_data_offsets_backward_matches_index >= 0
                                        and second_file_data_offset - files_data_offsets_backward_matches_index >= second_file_data_min_offset
                                    ):
                                        first_file_data_cell = first_file_data[first_file_data_offset - files_data_offsets_backward_matches_index]

                                        second_file_data_cell = second_file_data[second_file_data_offset - files_data_offsets_backward_matches_index]

                                        if first_file_data_cell != second_file_data_cell:
                                            break
                                        else:
                                            files_data_offsets_backward_matches_index += 1

                                    files_data_offsets_backward_matches_index -= 1

                                    if (
                                        first_file_data_min_possible_offset == -1
                                        or (
                                            first_file_data_offset - files_data_offsets_backward_matches_index < first_file_data_min_possible_offset
                                            or (
                                                first_file_data_offset - files_data_offsets_backward_matches_index == first_file_data_min_possible_offset
                                                and (
                                                    second_file_data_min_possible_offset == -1
                                                    or (
                                                        second_file_data_offset - files_data_offsets_backward_matches_index < second_file_data_min_possible_offset
                                                    )
                                                )
                                            )
                                        )
                                    ):
                                        files_data_offsets_backward_matches_min_possible_index = files_data_offsets_backward_matches_index

                                        first_file_data_min_possible_location = first_file_data_location
                                        first_file_data_min_possible_offset = first_file_data_offset

                                        second_file_data_min_possible_location = second_file_data_location
                                        second_file_data_min_possible_offset = second_file_data_offset

                                    # checking forward matches after the first match

                                    files_data_offsets_min_relative_matches_index = 1  # 0 already matches

                                    while files_data_offsets_min_relative_matches_index <= files_data_offsets_min_relative_matches:
                                        if (
                                            first_file_data_offset
                                            - files_data_offsets_backward_matches_index
                                            + files_data_offsets_min_relative_matches_index
                                            >= 0
                                            and
                                            first_file_data_offset
                                            - files_data_offsets_backward_matches_index
                                            + files_data_offsets_min_relative_matches_index
                                            <= first_file_data_size - 1
                                        ):
                                            first_file_data_cell = (
                                                first_file_data[
                                                    first_file_data_offset
                                                    - files_data_offsets_backward_matches_index
                                                    + files_data_offsets_min_relative_matches_index
                                                ]
                                            )
                                        else:
                                            first_file_data_cell = None

                                        if (
                                            second_file_data_offset
                                            - files_data_offsets_backward_matches_index
                                            + files_data_offsets_min_relative_matches_index
                                            >= 0
                                            and
                                            second_file_data_offset
                                            - files_data_offsets_backward_matches_index
                                            + files_data_offsets_min_relative_matches_index
                                            <= second_file_data_size - 1
                                        ):
                                            second_file_data_cell = (
                                                second_file_data[
                                                    second_file_data_offset
                                                    - files_data_offsets_backward_matches_index
                                                    + files_data_offsets_min_relative_matches_index
                                                ]
                                            )
                                        else:
                                            second_file_data_cell = None

                                        if (
                                            first_file_data_cell is None
                                            and second_file_data_cell is None
                                        ):
                                            break
                                        else:
                                            if (
                                                first_file_data_cell is None
                                                or second_file_data_cell is None
                                            ):
                                                error_found = True
                                            else:
                                                if first_file_data_cell != second_file_data_cell:
                                                    error_found = True

                                        if error_found is True:
                                            break
                                        else:
                                            files_data_offsets_min_relative_matches_index += 1

                                if error_found is True:
                                    error_found = False
                                else:
                                    method_found = True

                                if method_found is True:
                                    break
                                else:
                                    second_file_data_location += 1
                                    second_file_data_offset += 1

                                    if second_file_data_offset <= second_file_data_max_offset:
                                        second_file_data_cell = second_file_data[second_file_data_offset]
                                    else:
                                        second_file_data_cell = None

                                        first_file_data_location = first_file_data_min_location + files_data_offsets_current_resolution
                                        first_file_data_offset = first_file_data_min_offset + files_data_offsets_current_resolution

                                        if first_file_data_offset <= first_file_data_max_offset:
                                            first_file_data_cell = first_file_data[first_file_data_offset]

                                            second_file_data_location = second_file_data_min_location
                                            second_file_data_offset = second_file_data_min_offset

                                            if (
                                                second_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                                                and second_file_data_offset <= second_file_data_max_offset
                                            ):
                                                second_file_data_cell = second_file_data[second_file_data_offset]
                                            else:
                                                second_file_data_cell = None

                                            files_data_offsets_current_resolution = (
                                                int(
                                                    files_data_offsets_current_resolution
                                                    * (files_data_offsets_max_resolution_difference_percentage_gain + 100)
                                                    / 100
                                                )
                                            )

                                            if (
                                                files_data_offsets_current_resolution - files_data_offsets_last_resolution
                                                < files_data_offsets_min_resolution_difference_gain
                                            ):
                                                files_data_offsets_current_resolution = (
                                                    files_data_offsets_last_resolution +
                                                    files_data_offsets_min_resolution_difference_gain
                                                )
                                            else:
                                                if files_data_offsets_max_resolution_difference_gain > 0:
                                                    if (
                                                        files_data_offsets_current_resolution - files_data_offsets_last_resolution
                                                        > files_data_offsets_max_resolution_difference_gain
                                                    ):
                                                        files_data_offsets_current_resolution = (
                                                            files_data_offsets_last_resolution +
                                                            files_data_offsets_max_resolution_difference_gain
                                                        )

                                            files_data_offsets_last_resolution = files_data_offsets_current_resolution
                                        else:
                                            first_file_data_cell = None

                        if method_found is False:
                            # do an absolute files comparison with the relative files comparison parameters
                            # but look only for the min possible locations and offsets

                            if files_data_offsets_max_relative_differences >= 0:
                                first_file_data_max_location = first_file_data_min_location + files_data_offsets_max_relative_differences

                                if first_file_data_max_location >= first_file_data_min_location + (first_file_data_size - first_file_data_min_offset):
                                    first_file_data_max_location = first_file_data_min_location + (first_file_data_size - first_file_data_min_offset) - 1
                            else:
                                first_file_data_max_location = first_file_data_min_location + (first_file_data_size - first_file_data_min_offset) - 1

                            if files_data_offsets_max_relative_differences >= 0:
                                first_file_data_max_offset = first_file_data_min_offset + files_data_offsets_max_relative_differences

                                if first_file_data_max_offset >= first_file_data_size:
                                    first_file_data_max_offset = first_file_data_size - 1
                            else:
                                first_file_data_max_offset = first_file_data_size - 1

                            if files_data_offsets_max_relative_differences >= 0:
                                second_file_data_max_location = second_file_data_min_location + files_data_offsets_max_relative_differences

                                if second_file_data_max_location >= second_file_data_min_location + (second_file_data_size - second_file_data_min_offset):
                                    second_file_data_max_location = second_file_data_min_location + (second_file_data_size - second_file_data_min_offset) - 1
                            else:
                                second_file_data_max_location = second_file_data_min_location + (second_file_data_size - second_file_data_min_offset) - 1

                            if files_data_offsets_max_relative_differences >= 0:
                                second_file_data_max_offset = second_file_data_min_offset + files_data_offsets_max_relative_differences

                                if second_file_data_max_offset >= second_file_data_size:
                                    second_file_data_max_offset = second_file_data_size - 1
                            else:
                                second_file_data_max_offset = second_file_data_size - 1

                            # already checked the ones before the files data offsets max absolute differences in the absolute files comparison

                            first_file_data_location = first_file_data_min_location + 1
                            first_file_data_offset = first_file_data_min_offset + 1

                            if files_data_offsets_max_absolute_differences > 0:
                                first_file_data_location += files_data_offsets_max_absolute_differences
                                first_file_data_offset += files_data_offsets_max_absolute_differences

                            if (
                                first_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                                and first_file_data_offset <= first_file_data_max_offset
                            ):
                                first_file_data_cell = first_file_data[first_file_data_offset]
                            else:
                                first_file_data_cell = None

                            second_file_data_location = second_file_data_min_location + 1
                            second_file_data_offset = second_file_data_min_offset + 1

                            if files_data_offsets_max_absolute_differences > 0:
                                second_file_data_location += files_data_offsets_max_absolute_differences
                                second_file_data_offset += files_data_offsets_max_absolute_differences

                            if (
                                second_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                                and second_file_data_offset <= second_file_data_max_offset
                            ):
                                second_file_data_cell = second_file_data[second_file_data_offset]
                            else:
                                second_file_data_cell = None

                            while (
                                first_file_data_offset <= first_file_data_max_offset
                                and second_file_data_offset <= second_file_data_max_offset
                                and (
                                    first_file_data_min_possible_offset == -1
                                    or (
                                        first_file_data_offset < first_file_data_min_possible_offset
                                        or (
                                            first_file_data_offset == first_file_data_min_possible_offset
                                            and (
                                                second_file_data_min_possible_offset == -1
                                                or (
                                                    second_file_data_offset < second_file_data_min_possible_offset
                                                )
                                            )
                                        )
                                    )
                                )
                            ):
                                if first_file_data_cell != second_file_data_cell:
                                    error_found = True
                                else:
                                    # checking the first match location
                                    # (no need to actually check because in absolute files comparison the first found match is the first match)

                                    files_data_offsets_backward_matches_index = 0

                                    if (
                                        first_file_data_min_possible_offset == -1
                                        or (
                                            first_file_data_offset - files_data_offsets_backward_matches_index < first_file_data_min_possible_offset
                                            or (
                                                first_file_data_offset - files_data_offsets_backward_matches_index == first_file_data_min_possible_offset
                                                and (
                                                    second_file_data_min_possible_offset == -1
                                                    or (
                                                        second_file_data_offset - files_data_offsets_backward_matches_index < second_file_data_min_possible_offset
                                                    )
                                                )
                                            )
                                        )
                                    ):
                                        files_data_offsets_backward_matches_min_possible_index = files_data_offsets_backward_matches_index

                                        first_file_data_min_possible_location = first_file_data_location
                                        first_file_data_min_possible_offset = first_file_data_offset

                                        second_file_data_min_possible_location = second_file_data_location
                                        second_file_data_min_possible_offset = second_file_data_offset

                                if error_found is True:
                                    error_found = False
                                else:
                                    method_found = True

                                if method_found is True:
                                    break
                                else:
                                    first_file_data_location += 1
                                    first_file_data_offset += 1

                                    if first_file_data_offset <= first_file_data_max_offset:
                                        first_file_data_cell = first_file_data[first_file_data_offset]
                                    else:
                                        first_file_data_cell = None

                                    second_file_data_location += 1
                                    second_file_data_offset += 1

                                    if second_file_data_offset <= second_file_data_max_offset:
                                        second_file_data_cell = second_file_data[second_file_data_offset]
                                    else:
                                        second_file_data_cell = None

                            if method_found is True:
                                # going to the first found match because we'll meet the next one later on anyway

                                if (
                                    first_file_data_min_possible_location != -1
                                    and first_file_data_min_possible_offset != -1
                                    and second_file_data_min_possible_location != -1
                                    and second_file_data_min_possible_offset != -1
                                ):
                                    files_data_offsets_backward_matches_index = files_data_offsets_backward_matches_min_possible_index

                                    first_file_data_location = first_file_data_min_possible_location
                                    first_file_data_offset = first_file_data_min_possible_offset

                                    second_file_data_location = second_file_data_min_possible_location
                                    second_file_data_offset = second_file_data_min_possible_offset

                        if method_found is False:
                            # going to the first found match if there is one because haven't found a suitable match

                            if (
                                first_file_data_min_possible_location != -1
                                and first_file_data_min_possible_offset != -1
                                and second_file_data_min_possible_location != -1
                                and second_file_data_min_possible_offset != -1
                            ):
                                files_data_offsets_backward_matches_index = files_data_offsets_backward_matches_min_possible_index

                                first_file_data_location = first_file_data_min_possible_location
                                first_file_data_offset = first_file_data_min_possible_offset

                                second_file_data_location = second_file_data_min_possible_location
                                second_file_data_offset = second_file_data_min_possible_offset

                                method_found = True

                        if method_found is True:
                            method_found = False

                            # going to the first match

                            if files_data_offsets_backward_matches_index > 0:
                                first_file_data_location -= files_data_offsets_backward_matches_index
                                first_file_data_offset -= files_data_offsets_backward_matches_index

                                if first_file_data_offset >= 0:
                                    first_file_data_cell = first_file_data[first_file_data_offset]
                                else:
                                    first_file_data_cell = None

                                second_file_data_location -= files_data_offsets_backward_matches_index
                                second_file_data_offset -= files_data_offsets_backward_matches_index

                                if second_file_data_offset >= 0:
                                    second_file_data_cell = second_file_data[second_file_data_offset]
                                else:
                                    second_file_data_cell = None

                            # going to the last difference

                            first_file_data_location -= 1
                            first_file_data_offset -= 1

                            if first_file_data_offset >= 0:
                                first_file_data_cell = first_file_data[first_file_data_offset]
                            else:
                                first_file_data_cell = None

                            second_file_data_location -= 1
                            second_file_data_offset -= 1

                            if second_file_data_offset >= 0:
                                second_file_data_cell = second_file_data[second_file_data_offset]
                            else:
                                second_file_data_cell = None

                            # if first_file_data_location < first_file_data_min_location:
                            #    first_file_data_min_location = first_file_data_location

                            # if first_file_data_offset < first_file_data_min_offset:
                            #    first_file_data_min_offset = first_file_data_offset

                            # if second_file_data_location < second_file_data_min_location:
                            #    second_file_data_min_location = second_file_data_location

                            # if second_file_data_offset < second_file_data_min_offset:
                            #    second_file_data_min_offset = second_file_data_offset
                        else:
                            # going to the max possible locations and offsets since everything are differences

                            first_file_data_location = first_file_data_max_possible_location
                            first_file_data_offset = first_file_data_max_possible_offset

                            if first_file_data_offset >= 0:  # for sure bigger than 0, but just for reference
                                first_file_data_cell = first_file_data[first_file_data_offset]
                            else:
                                first_file_data_cell = None

                            second_file_data_location = second_file_data_max_possible_location
                            second_file_data_offset = second_file_data_max_possible_offset

                            if second_file_data_offset >= 0:  # for sure bigger than 0, but just for reference
                                second_file_data_cell = second_file_data[second_file_data_offset]
                            else:
                                second_file_data_cell = None

                        if (
                            first_file_data_min_offset >= 0  # for sure bigger than 0, but just for reference
                            and first_file_data_min_offset <= first_file_data_offset
                        ):
                            first_file_data_cell = first_file_data[first_file_data_min_offset]
                        else:
                            first_file_data_cell = None

                        first_file_data_location_index = first_file_data_min_location
                        first_file_data_offset_index = first_file_data_min_offset

                        if (
                            second_file_data_min_offset >= 0  # for sure bigger than 0, but just for reference
                            and second_file_data_min_offset <= second_file_data_offset
                        ):
                            second_file_data_cell = second_file_data[second_file_data_min_offset]
                        else:
                            second_file_data_cell = None

                        second_file_data_location_index = second_file_data_min_location
                        second_file_data_offset_index = second_file_data_min_offset

                        while (
                            first_file_data_offset_index <= first_file_data_offset
                            or second_file_data_offset_index <= second_file_data_offset
                        ):
                            difference = (
                                add_comparison(
                                    first_file_data_location_index
                                    , first_file_data_cell
                                    , second_file_data_location_index
                                    , second_file_data_cell
                                    , show_differences
                                    , 1
                                )
                            )

                            differences.append(difference)

                            differences_amount += 1

                            if first_file_data_offset_index <= first_file_data_offset:
                                first_file_data_location_index += 1
                                first_file_data_offset_index += 1

                                if (
                                    first_file_data_offset_index >= 0  # for sure bigger than 0, but just for reference
                                    and first_file_data_offset_index <= first_file_data_offset
                                ):
                                    first_file_data_cell = first_file_data[first_file_data_offset_index]
                                else:
                                    first_file_data_cell = None
                            else:
                                first_file_data_cell = None

                            if second_file_data_offset_index <= second_file_data_offset:
                                second_file_data_location_index += 1
                                second_file_data_offset_index += 1

                                if (
                                    second_file_data_offset_index >= 0  # for sure bigger than 0, but just for reference
                                    and second_file_data_offset_index <= second_file_data_offset
                                ):
                                    second_file_data_cell = second_file_data[second_file_data_offset_index]
                                else:
                                    second_file_data_cell = None
                            else:
                                second_file_data_cell = None

                        method_found = True

                    if method_found is True:  # will always hit
                        method_found = False

                    if first_file_data_offset < first_file_data_size:
                        first_file_data_location += 1
                        first_file_data_offset += 1

                        if (
                            first_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                            and first_file_data_offset < first_file_data_size
                        ):
                            first_file_data_cell = first_file_data[first_file_data_offset]
                        else:
                            first_file_data_cell = None
                    else:
                        first_file_data_cell = None

                    if second_file_data_offset < second_file_data_size:
                        second_file_data_location += 1
                        second_file_data_offset += 1

                        if (
                            second_file_data_offset >= 0  # for sure bigger than 0, but just for reference
                            and second_file_data_offset < second_file_data_size
                        ):
                            second_file_data_cell = second_file_data[second_file_data_offset]
                        else:
                            second_file_data_cell = None
                    else:
                        second_file_data_cell = None

                if first_file_data_size - first_file_data_offset > 0:
                    ff.seek(
                        (first_file_data_size - first_file_data_offset) * -1
                        , os.SEEK_CUR
                    )

                if second_file_data_size - second_file_data_offset > 0:
                    sf.seek(
                        (second_file_data_size - second_file_data_offset) * -1
                        , os.SEEK_CUR
                    )

            print('finished comparing files')

    if matches_amount > 0:
        matches_sequences = combine_comparisons(matches, 0)
        matches_sequences_amount = len(matches_sequences)

    if differences_amount > 0:
        differences_sequences = combine_comparisons(differences, 1)
        differences_sequences_amount = len(differences_sequences)

    print("")
    print(
        "Found" + ' ' + str(matches_amount) + ' ' + "matches"
        + ',' + ' ' + "and" + ' ' + str(matches_sequences_amount) + ' ' + "matches sequences"
    )

    print(
        "Found" + ' ' + str(differences_amount) + ' ' + "differences"
        + ',' + ' ' + "and" + ' ' + str(differences_sequences_amount) + ' ' + "differences sequences"
    )

    output_file_data_list = []

    Headers = []

    Headers.append("First File Path")
    Headers.append("Second File Path")
    Headers.append("Output File Path")

    Fields = []

    Fields.append(Headers[0] + ':' + ' ' + first_file_path)
    Fields.append(Headers[1] + ':' + ' ' + second_file_path)
    Fields.append(Headers[2] + ':' + ' ' + output_file_path)

    for Field in Fields:
        output_file_data_list.append(Field)

    output_file_data_list.append("")

    Headers = []

    Headers.append("Found matches")
    Headers.append("Found matches sequences")
    Headers.append("Found differences")
    Headers.append("Found differences sequences")

    Fields = []

    Fields.append(Headers[0] + ':' + ' ' + str(matches_amount))
    Fields.append(Headers[1] + ':' + ' ' + str(matches_sequences_amount))
    Fields.append(Headers[2] + ':' + ' ' + str(differences_amount))
    Fields.append(Headers[3] + ':' + ' ' + str(differences_sequences_amount))

    for Field in Fields:
        output_file_data_list.append(Field)

    if (
        (show_matches is True and matches_sequences_amount > 0)
        or (show_differences is True and differences_sequences_amount > 0)
    ):
        matches_sequences_index = 0

        match = None
        match_first_file_data_location = None
        match_first_file_data_bytes = None
        match_first_file_data_bytes_size = None
        match_second_file_data_location = None

        differences_sequences_index = 0

        difference = None
        difference_first_file_data_location = None
        difference_first_file_data_bytes = None
        difference_first_file_data_bytes_size = None
        difference_second_file_data_location = None
        difference_second_file_data_bytes = None
        difference_second_file_data_bytes_size = None  # not needed in an absolute files comparison, only in a relative files comparison

        if args.verbose is True:
            print("")

        output_file_data_list.append("")

        Matches_Headers = []

        Matches_Headers.append("Type")
        Matches_Headers.append("First Location")
        Matches_Headers.append("Second Location")
        Matches_Headers.append("Data")
        Matches_Headers.append("Size")

        Matches_Fields = []

        Matches_Fields.append(None)
        Matches_Fields.append(None)
        Matches_Fields.append(None)
        Matches_Fields.append(None)
        Matches_Fields.append(None)

        Differences_Headers = []

        Differences_Headers.append("Type")
        Differences_Headers.append("First Location")
        Differences_Headers.append("Second Location")
        Differences_Headers.append("First Data")
        Differences_Headers.append("Second Data")

        if files_comparison_type != 0:
            Differences_Headers.append("First Data Size")
            Differences_Headers.append("Second Data Size")
        else:
            Differences_Headers.append("Size")

        Differences_Fields = []

        Differences_Fields.append(None)
        Differences_Fields.append(None)
        Differences_Fields.append(None)
        Differences_Fields.append(None)
        Differences_Fields.append(None)

        if files_comparison_type != 0:
            Differences_Fields.append(None)
            Differences_Fields.append(None)
        else:
            Differences_Fields.append(None)

        if show_matches is True:
            if matches_sequences_index < matches_sequences_amount:
                match = matches_sequences[matches_sequences_index]
            else:
                match = None

        if show_differences is True:
            if differences_sequences_index < differences_sequences_amount:
                difference = differences_sequences[differences_sequences_index]
            else:
                difference = None

        while (
            (show_matches is True and matches_sequences_index < matches_sequences_amount)
            or (show_differences is True and differences_sequences_index < differences_sequences_amount)
        ):
            if show_matches is True:
                if match is not None:
                    match_first_file_data_location = match[0]
                    match_first_file_data_bytes = match[1]
                    match_first_file_data_bytes_size = match[2]
                    match_second_file_data_location = match[3]
                else:
                    match_first_file_data_location = None
                    match_first_file_data_bytes = None
                    match_first_file_data_bytes_size = None
                    match_second_file_data_location = None

            if show_differences is True:
                if difference is not None:
                    difference_first_file_data_location = difference[0]
                    difference_first_file_data_bytes = difference[1]
                    difference_first_file_data_bytes_size = difference[2]
                    difference_second_file_data_location = difference[3]
                    difference_second_file_data_bytes = difference[4]

                    if files_comparison_type != 0:
                        difference_second_file_data_bytes_size = difference[5]
                else:
                    difference_first_file_data_location = None
                    difference_first_file_data_bytes = None
                    difference_first_file_data_bytes_size = None
                    difference_second_file_data_location = None
                    difference_second_file_data_bytes = None

                    if files_comparison_type != 0:
                        difference_second_file_data_bytes_size = None

            if (
                show_matches is True
                and (
                    show_differences is False
                    or (
                        match_first_file_data_location is not None
                        and (
                            difference_first_file_data_location is None
                            or (
                                match_first_file_data_location < difference_first_file_data_location
                                or (
                                    match_first_file_data_location == difference_first_file_data_location
                                    and (
                                        match_first_file_data_bytes_size is not None
                                        and (
                                            difference_first_file_data_bytes_size is None
                                            or (
                                                match_first_file_data_bytes_size < difference_first_file_data_bytes_size
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ):
                Matches_Fields[0] = Matches_Headers[0] + ':' + ' ' + "Matches"
                Matches_Fields[1] = Matches_Headers[1] + ':' + ' ' + CheckHexText(match_first_file_data_location, AddressesLength, True)
                Matches_Fields[2] = Matches_Headers[2] + ':' + ' ' + CheckHexText(match_second_file_data_location, AddressesLength, True)
                Matches_Fields[3] = (
                    Matches_Headers[3] + ':' + ' ' + (
                        "N/A" if match_first_file_data_bytes_size == 0 else (
                            "0x" + ''.join(match_first_file_data_bytes)
                        )
                    )
                )

                Matches_Fields[4] = Matches_Headers[4] + ':' + ' ' + CheckHexText(match_first_file_data_bytes_size, SizeLength, True)

                output_file_data_list_cell = '\t'.join(Matches_Fields)

                if matches_sequences_index < matches_sequences_amount:
                    matches_sequences_index += 1

                    if matches_sequences_index < matches_sequences_amount:
                        match = matches_sequences[matches_sequences_index]
                    else:
                        match = None
                else:
                    match = None
            else:
                Differences_Fields[0] = Differences_Headers[0] + ':' + ' ' + "Differences"
                Differences_Fields[1] = Differences_Headers[1] + ':' + ' ' + CheckHexText(difference_first_file_data_location, AddressesLength, True)
                Differences_Fields[2] = Differences_Headers[2] + ':' + ' ' + CheckHexText(difference_second_file_data_location, AddressesLength, True)
                Differences_Fields[3] = (
                    Differences_Headers[3] + ':' + ' ' + (
                        "N/A" if difference_first_file_data_bytes_size == 0 else (
                            "0x" + ''.join(difference_first_file_data_bytes)
                        )
                    )
                )

                Differences_Fields[4] = (
                    Differences_Headers[4] + ':' + ' ' + (
                        "N/A" if difference_second_file_data_bytes_size == 0 else (
                            "0x" + ''.join(difference_second_file_data_bytes)
                        )
                    )
                )

                Differences_Fields[5] = Differences_Headers[5] + ':' + ' ' + CheckHexText(difference_first_file_data_bytes_size, SizeLength, True)

                if files_comparison_type != 0:
                    Differences_Fields[6] = Differences_Headers[6] + ':' + ' ' + CheckHexText(difference_second_file_data_bytes_size, SizeLength, True)

                output_file_data_list_cell = '\t'.join(Differences_Fields)

                if differences_sequences_index < differences_sequences_amount:
                    differences_sequences_index += 1

                    if differences_sequences_index < differences_sequences_amount:
                        difference = differences_sequences[differences_sequences_index]
                    else:
                        difference = None
                else:
                    difference = None

            output_file_data_list.append(output_file_data_list_cell)

            if args.verbose is True:
                print(output_file_data_list_cell)

    output_file_data = "\r\n".join(output_file_data_list)

    if args.dry_run is False:
        with open(output_file_path, 'w') as crf:
            crf.write(output_file_data)

    print("")
    print('finished processing:' + ' ' + output_file_path)


main()
