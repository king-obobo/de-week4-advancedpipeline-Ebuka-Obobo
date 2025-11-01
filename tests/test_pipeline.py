import pytest
from unittest.mock import patch, MagicMock
from pipeline.pipeline import Pipeline



@patch("pipeline.pipeline.Exporter")
@patch("pipeline.pipeline.Analyzer")
@patch("pipeline.pipeline.DataEnricher")
@patch("pipeline.pipeline.APIClient")
def test_pipeline_run_success(mock_api_client, mock_data_enricher, mock_analyzer, mock_exporter):
    # We start withe mocking the APIClient
    mock_api_instance = MagicMock()
    mock_api_instance.get_all_products.return_value = [{"id", 1}, {"price": 100}]
    mock_api_instance.get_all_users.return_value = [{"id", 1}, {"user_name": "test"}]
    mock_api_client.return_value = mock_api_instance
    
    # Next we mock the DataEnricher
    mock_enricher_instance = MagicMock()
    mock_enricher_instance.enrich_data.return_value = "fake_df"
    mock_data_enricher.return_value = mock_enricher_instance
    
    # Next Our Analyzer
    mock_analyzer_instance = MagicMock()
    mock_analyzer_instance.perform_analysis.return_value = {"user_name": {}, "total_revenue": {}}
    mock_analyzer.return_value = mock_analyzer_instance
    
    # Finally, our expprter
    mock_exporter_instance = MagicMock()
    mock_exporter.return_value = mock_exporter_instance
    
    # We run our pipeline
    
    pipeline = Pipeline()
    pipeline.run()
    
    # Assertions
    mock_api_instance.get_all_products.assert_called_once()
    mock_api_instance.get_all_users.assert_called_once()
    mock_enricher_instance.enrich_data.assert_called_once()
    mock_analyzer.assert_called_once_with("fake_df")
    mock_analyzer_instance.perform_analysis.assert_called_once()
    mock_exporter.assert_called_once_with({"user_name": {}, "total_revenue": {}})
    mock_exporter_instance.export_to_json.assert_called_once()
    
@patch("pipeline.pipeline.APIClient")
def test_pipeline_run_handles_exception(mock_api_client, capsys):
    mock_api_client.side_effect = Exception("API failure")

    pipeline = Pipeline()
    pipeline.run()

    captured = capsys.readouterr()
    assert "An error occured: API failure" in captured.out

    