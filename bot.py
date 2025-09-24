class PriceCrossBot:
    def __init__(self):
        pass

    def crossing(self, price, level):
        """Check if price == level"""
        import pandas as pd
        result = price == level
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def crossing_up(self, prev_price, price, level):
        """Price crosses from below to above level"""
        import pandas as pd
        result = (prev_price < level) & (price >= level)
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def crossing_down(self, prev_price, price, level):
        """Price crosses from above to below level"""
        import pandas as pd
        result = (prev_price > level) & (price <= level)
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def greater_than(self, price, level):
        import pandas as pd
        result = price > level
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def less_than(self, price, level):
        import pandas as pd
        result = price < level
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def inside_channel(self, price, lower, upper):
        import pandas as pd
        result = (price >= lower) & (price <= upper)
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def outside_channel(self, price, lower, upper):
        import pandas as pd
        result = (price < lower) | (price > upper)
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def entering_channel(self, prev_price, price, lower, upper):
        """Price moves from outside into the channel"""
        import pandas as pd
        result = ((prev_price < lower) & (price >= lower) & (price <= upper)) | \
                 ((prev_price > upper) & (price >= lower) & (price <= upper))
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def exiting_channel(self, prev_price, price, lower, upper):
        """Price moves from inside channel to outside"""
        import pandas as pd
        result = ((prev_price >= lower) & (prev_price <= upper)) & ((price < lower) | (price > upper))
        if isinstance(result, pd.Series):
            return result.any()
        return result

    def moving_up(self, prev_price, price):
        return price > prev_price

    def moving_down(self, prev_price, price):
        return price < prev_price

    def moving_up_percent(self, prev_price, price):
        if prev_price == 0: 
            return 0
        return ((price - prev_price) / prev_price) * 100 if price > prev_price else 0

    def moving_down_percent(self, prev_price, price):
        if prev_price == 0: 
            return 0
        return ((prev_price - price) / prev_price) * 100 if price < prev_price else 0
