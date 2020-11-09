CREATE TABLE IF NOT EXISTS model_response
(
    id INT NOT NULL AUTO_INCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_id INT,
    store_id INT,
    y_score FLOAT,
    x_raw LONGTEXT,
    x LONGTEXT,
    execution_time FLOAT,
    version VARCHAR(8),
    PRIMARY KEY(id)
);
