from stock_market_platform.utils.mongo_connection import StockMarketDBConnector

connector = StockMarketDBConnector("financial_statements")


def filter_by_statement_type(statement_type):
    return [
        document
        for document in connector.collection.find(
            {"metadata.statement_type": statement_type}
        )
    ]


def get_gross_margin():
    return [
        document
        for document in connector.collection.aggregate(
            pipeline=[
                {
                    "$match": {
                        "$and": [
                            {"metadata.statement_type": "income_statement"},
                            {"data.total_revenue": {"$ne": "0"}},
                            {"data.gross_profit": {"$ne": "0"}},
                        ]
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "metadata.symbol": 1,
                        "gross_margin": {
                            "$map": {
                                "input": "$data",
                                "as": "data",
                                "in": {
                                    "$divide": [
                                        {
                                            "$convert": {
                                                "input": {
                                                    "$reduce": {
                                                        "input": {
                                                            "$split": [
                                                                "$$data.gross_profit",
                                                                ",",
                                                            ]
                                                        },
                                                        "initialValue": "",
                                                        "in": {
                                                            "$concat": [
                                                                "$$value",
                                                                "$$this",
                                                            ]
                                                        },
                                                    }
                                                },
                                                "to": "int",
                                                "onError": 1,
                                            }
                                        },
                                        {
                                            "$convert": {
                                                "input": {
                                                    "$reduce": {
                                                        "input": {
                                                            "$split": [
                                                                "$$data.total_revenue",
                                                                ",",
                                                            ]
                                                        },
                                                        "initialValue": "",
                                                        "in": {
                                                            "$concat": [
                                                                "$$value",
                                                                "$$this",
                                                            ]
                                                        },
                                                    }
                                                },
                                                "to": "int",
                                                "onError": 1,
                                            }
                                        },
                                    ]
                                },
                            }
                        },
                    }
                },
            ]
        )
    ]
