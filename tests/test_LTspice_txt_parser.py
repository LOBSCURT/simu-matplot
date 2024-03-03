import LTspice_txt_parser



def test_simple_1_trace_test_case():
    test_input = ['time\tV(n005)\n',
                  '0.000000000000000e+00\t2.500000e+00\n',
                  '2.072000000511463e-09\t2.500000e+00\n',
                  '6.316353223183249e-08\t2.499983e+00\n']
    expected_output = [
                         ["s", "V", None],
                         [
                             [0.0,
                              2.072000000511463e-09,
                              6.316353223183249e-08],
                             [2.5, 2.5, 2.499983],
                             []
                         ]]

    assert LTspice_txt_parser.LTspice_read_txt(test_input) == expected_output

def test_simple_2_trace_test_case():
    test_input = ['time\tV(n005)\tV(n007)\n',
                  '0.000000000000000e+00\t2.500000e+00\t2.500000e+00\n',
                  '2.072000000511463e-09\t2.500000e+00\t2.500000e+00\n',
                  '6.316353223183249e-08\t2.499983e+00\t2.500264e+00\n']
    expected_output = [
                         ["s", "V", "V"],
                         [
                            [0.0,
                             2.072000000511463e-09,
                             6.316353223183249e-08],
                            [2.5, 2.5, 2.499983],
                            [2.5, 2.5, 2.500264]
                         ]]

    assert LTspice_txt_parser.LTspice_read_txt(test_input) == expected_output

