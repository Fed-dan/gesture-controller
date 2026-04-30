from src.vision.smoother import CoordinateSmoother

def test_first_call_returns_unchanged():
    coordinate_smoother = CoordinateSmoother(alpha=0.5)
    assert coordinate_smoother.smooth(1, 2) == (1, 2)

def test_smoothing_applied():
    coordinate_smoother = CoordinateSmoother(alpha=0.5)
    coordinate_smoother.smooth(1, 2)
    assert coordinate_smoother.smooth(3, 4) == (2, 3)

def test_alpha_one_no_smoothing():
    coordinate_smoother = CoordinateSmoother(alpha=1.0)
    assert coordinate_smoother.smooth(1, 2) == (1, 2)