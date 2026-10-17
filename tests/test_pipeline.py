from ml.data_pipeline import load_raw_dataset

def test_load_data():
    df = load_raw_dataset()
    assert len(df) == 20
    assert "id" in df.columns
    assert "value" in df.columns