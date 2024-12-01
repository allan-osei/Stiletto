//+------------------------------------------------------------------+
//|                                                stiletto-auto.mq5 |
//|                                 Copyright 2024, Theorangeteam.com|
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2023, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
#include <JAson.mqh>
#include <Trade\Trade.mqh>
#include <Trade\OrderInfo.mqh> // Instatiate Library for Orders Information
#include <Trade\PositionInfo.mqh>

CTrade m_trade;
ulong order_magic = 60262;
#property script_show_inputs
//--- input parameters
input string Webhook_Url = "";
input int slippage = 200;
input double lot_size = 0.01;

struct ticket
{
    int td; // if the difference between the current price and the sl is >= ts, adjust the sl to be td distance from the price
    int ts;
    double tt;
    ulong tid;
    bool active;
    int val_type; // percentages, points, 1, -1
};

int db = DatabaseOpen("exo.sqlite", DATABASE_OPEN_READWRITE | DATABASE_OPEN_CREATE | DATABASE_OPEN_COMMON);

int OnInit()
{
    if (db == INVALID_HANDLE)
    {
        Print("DB: ", "exo.sqlite", " open failed with code ", GetLastError());
        return -1;
    }
    
    if (!DatabaseTableExists(db, "TICKETS"))
    {
        if (!DatabaseExecute(db, "CREATE TABLE TICKETS("
                                "ID INT PRIMARY KEY NOT NULL,"
                                "tid INT NOT NULL,"
                                "tt INT NOT NULL,"
                                "td INT NOT NULL,"
                                "ts INT NOT NULL,"
                                "active INT NOT NULL);"))
        {
            Print("DB: create the TICKETS table failed with code ", GetLastError());
            return false;
        }
    }
    
    EventSetTimer(5);
    return (INIT_SUCCEEDED);
}

void OnDeinit(const int reason)
{
    EventKillTimer();
    DatabaseClose(db);
}

void remove_ticket(ulong tid)
{
    string query = StringFormat("DELETE FROM TICKETS WHERE tid = %d", tid);
    if (!DatabaseExecute(db, query))
    {
        Print("DB: delete from the TICKETS table failed with code ", GetLastError());
    }
}

int getticketbyid(ticket &t, ulong tid)
{
    string query = StringFormat("SELECT * FROM TICKETS WHERE tid = %d", tid);
    int request = DatabasePrepare(db, query);
    
    if (request == INVALID_HANDLE)
    {
        Print("DB: ", "exo", " request failed with code ", GetLastError());
        DatabaseClose(db);
        return -1;
    }
    
    DatabaseReadBind(request, t);
    DatabaseFinalize(request);
    return 1;
}

void activate_trailing(ulong tid)
{
    string query = StringFormat("UPDATE TICKETS SET active = 1 WHERE tid = %d", tid);
    if (!DatabaseExecute(db, query))
    {
        Print("DB: update the TICKETS table failed with code ", GetLastError());
    }
}

void OnTimer()
{
    string cookie = NULL, headers;
    string url = Webhook_Url;
    char post[], result[];
    ResetLastError();
    int timeout = 5000;
    int res = WebRequest("GET", url, cookie, NULL, timeout, post, 0, result, headers);
    
    if (res == -1)
    {
        Print("Error in WebRequest. Error code =", GetLastError());
    }
    else
    {
        if (res == 200)
        {
            CJAVal loader;
            loader.Deserialize(CharArrayToString(result), CP_UTF8);
            double e = loader["entry"].ToDbl();
            double tp = loader["tp"].ToDbl();
            double sl = loader["sl"].ToDbl();
            double tt = loader["tt"].ToDbl();
            double ts = loader["ts"].ToDbl();
            double td = loader["td"].ToDbl();
            string t = loader["ticker"].ToStr();
            string s = loader["side"].ToStr();
            ulong qt = loader["q_type"].ToInt();
            ulong m = loader["magic"].ToInt();
            string command = loader["command"].ToStr();
            
            Print("Received command: ", command);

            if (command == "NEW") 
            {
                if (m > 0) {
                    m_trade.SetExpertMagicNumber(m);
                } else {
                    m_trade.SetExpertMagicNumber(order_magic);
                }

                m_trade.SetMarginMode();
                m_trade.SetTypeFillingBySymbol(t);
                m_trade.SetDeviationInPoints(slippage);

                if (s == "BUY" || s == "buy") {
                    if (m_trade.Buy(lot_size, t, e, sl, tp, "q")) {
                        Print("Order placed: Buy ", t, " at ", e, " SL: ", sl, " TP: ", tp);
                    } else {
                        Print("Error placing buy order: ", GetLastError());
                    }
                } else if (s == "SELL" || s == "sell") {
                    if (m_trade.Sell(lot_size, t, e, sl, tp, "q")) {
                        Print("Order placed: Sell ", t, " at ", e, " SL: ", sl, " TP: ", tp);
                    } else {
                        Print("Error placing sell order: ", GetLastError());
                    }
                }
            } 
            else if (command == "STOP") 
            {
                if (t == "") {
                    close_all();
                } else {
                    close_by_ticker(t);
                }
            } 
            else if (command == "MODIFY") 
            {
                for (int v = PositionsTotal() - 1; v >= 0; v--) 
                {
                    CPositionInfo m_position;
                    ulong posticket = PositionGetTicket(v);
                    if (m_position.SelectByIndex(v)) 
                    {
                        if (m_position.Symbol() == t || m_position.Magic() == m) 
                        {
                            CTrade trade;
                            double current_sl = PositionGetDouble(POSITION_SL);
                            double current_tp = PositionGetDouble(POSITION_TP);

                            if (tp != 0 && sl == 0) 
                            {
                                if (trade.PositionModify(posticket, current_sl, tp)) {
                                    Print("Take Profit Modified: ", posticket);
                                } else {
                                    Print("Error modifying take profit: ", GetLastError());
                                }
                            } 
                            else if (tp == 0 && sl != 0) 
                            {
                                if (trade.PositionModify(posticket, sl, current_tp)) {
                                    Print("Stop Loss Modified: ", posticket);
                                } else {
                                    Print("Error modifying stop loss: ", GetLastError());
                                }
                            } 
                            else if (tp != 0 && sl != 0) 
                            {
                                if (trade.PositionModify(posticket, sl, tp)) {
                                    Print("Stop loss and take profit modified: ", posticket);
                                } else {
                                    Print("Error modifying stop loss and take profit: ", GetLastError());
                                }
                            } 
                            else if (sl == -1) 
                            {
                                double open_price = PositionGetDouble(POSITION_PRICE_OPEN);
                                if (trade.PositionModify(posticket, open_price, current_tp)) {
                                    Print("Stop Loss Moved to Break-Even: ", posticket);
                                } else {
                                    Print("Error moving stop loss to break-even: ", GetLastError());
                                }
                            }
                        }
                    }
                }
            }
        } 
        else 
        {
            Print("Unexpected response code: ", res);
        }
    }
}

void OnTick()
{
    for (int i = PositionsTotal() - 1; i >= 0; i--)
    {
        ulong posticket = PositionGetTicket(i);
        if (PositionSelectByTicket(posticket))
        {
            ticket t;
            if (getticketbyid(t, posticket) == -1)
                continue; // Skip if ticket not found in the db
            
            if (t.tid == posticket && t.active) 
            {
                double current_price = SymbolInfoDouble(_Symbol, SYMBOL_BID);
                double current_sl = PositionGetDouble(POSITION_SL);
                double current_tp = PositionGetDouble(POSITION_TP);
                double open_price = PositionGetDouble(POSITION_PRICE_OPEN);
                double current_p = PositionGetDouble(POSITION_PRICE_CURRENT);
                
                if (t.val_type > 0 && open_price * ((t.tt + 100) / 100) >= current_price)
                {
                    if (MathAbs(current_p - open_price) > t.tt)
                    {
                        activate_trailing(posticket);
                    }
                }

                if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY)
                {
                    if (current_price - current_sl >= t.ts)
                    {
                        double sl = current_price - t.td;
                        if (sl > current_sl)
                        {
                            if (m_trade.PositionModify(posticket, sl, current_tp))
                            {
                                Print("Trailing stop modified: ", posticket);
                            }
                        }
                    }
                }
                else if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL)
                {
                    current_price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
                    if (current_sl - current_price >= t.ts)
                    {
                        double sl = current_price + t.td;
                        if (sl < current_sl)
                        {
                            if (m_trade.PositionModify(posticket, sl, current_tp))
                            {
                                Print("Trailing stop modified: ", posticket);
                            }
                        }
                    }
                }
            }
        }
    }
}

void close_by_ticker(string s)
{
    COrderInfo m_order;       // Library for Orders information
    CPositionInfo m_position; // Library for all position features and information

    for (int i = PositionsTotal() - 1; i >= 0; i--) // loop all Open Positions
    {
        if (m_position.SelectByIndex(i)) // select a position
        {
            if (m_position.Symbol() == s)
            {
                m_trade.PositionClose(m_position.Ticket()); // then close it
                Sleep(100); // Relax for 100 ms
            }
        }
    }
}

void close_all()
{
    COrderInfo m_order;       // Library for Orders information
    CPositionInfo m_position; // Library for all position features and information

    for (int i = PositionsTotal() - 1; i >= 0; i--) // loop all Open Positions
    {
        if (m_position.SelectByIndex(i)) // select a position
        {
            m_trade.PositionClose(m_position.Ticket()); // then close it
            Sleep(100); // Relax for 100 ms
        }
    }
}

void OnTrade()
{
    for (int i = PositionsTotal() - 1; i >= 0; i--)
    {
        ulong posticket = PositionGetTicket(i);
        if (PositionSelectByTicket(posticket))
        {
            if (PositionGetInteger(POSITION_TICKET) != 0)
            {
                remove_ticket(posticket);
            }
        }
    }
}
