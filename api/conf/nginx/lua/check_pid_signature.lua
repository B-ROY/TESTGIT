--doc see http://wiki.nginx.org/HttpCoreModule#.24uri


function catch(what)
   return what[1]
end

function try(what)
   status, result = pcall(what[1])
   if not status then
      what[2](result)
   end
   return result
end

local ok = nil
local pid = nil
local sig = nil
local doc = nil
local timestamp = 0 

local req_method = ngx.var.request_method
local expire_time = 60 * 30

-- 
-- local secret = "821l1i1x3fv8vs3dxlj1v2x91jqfs3om"
-- 
-- heydo gen secret key for client auth 
local secret = "6e1c51bfffc79c7932c0bb986cd29ce5"
local args = ngx.req.get_uri_args()

-- Get auth params
if req_method == "GET" then
    pid = ngx.var.arg_pid
    sig = ngx.var.arg__s_
    timestamp = ngx.var.arg__t_
    doc = ngx.var.arg_doc
elseif  req_method == "POST" or req_method == "PUT" or  req_method == "DELETE" then
    try {
        function()
            ngx.req.read_body()
            local post_args = ngx.req.get_post_args()
            args = post_args
            pid = post_args.pid
            sig = post_args._s_
            timestamp = post_args._t_
            doc = post_args.doc
        end,
        catch {
              function(error)

              end
        }
    }

    if not sig then
        sig=ngx.var.arg__s_
    end

    if not timestamp then
        timestamp = ngx.var.arg__t_
    end

    if not doc then
        doc = ngx.var.arg_doc
    end


else
    ngx.exit(ngx.HTTP_FORBIDDEN)
end

-- ***** doc debug *****
if doc then
    return 
end

if not timestamp or timestamp == ""  then
    ngx.exit(ngx.HTTP_FORBIDDEN)
end

if not sig or sig == "" then 
    ngx.exit(ngx.HTTP_FORBIDDEN)
end


local filter_args = ""
local key_table = {}  
--取出所有的键  
for key,_ in pairs(args) do  
    table.insert(key_table,key)
end  
--对所有键进行排序  
table.sort(key_table)  
for _,key in pairs(key_table) do
    if key ~= "_s_"  and key ~= "_t_"  then
        filter_args = filter_args .. key .. "=" ..args[key]
    end
end

-- args = 
-- local filter_args, n, err = ngx.re.sub(args, "(&|\\?)_s_=[^&]*&?", "")
-- if filter_args then
-- else
--     filter_args = args
-- end

-- local new_filter_args, nn, eerr = ngx.re.sub(filter_args, "(&|\\?)_t_=[^&]*&?", "")
-- if new_filter_args then
--     filter_args = new_filter_args
-- else
--     if not filter_args then
--         filter_args = args
--     end
-- end
--
-- ngx.log(ngx.ERR, ngx.var.uri)
-- ngx.log(ngx.ERR, filter_args)

local blocks = {
    a = "bc0113cee17f3df530f3e1c9d2ff7d5d",
    b = "ccb4b879bf5140b493ed6e2b33c5dcf7",
    c = "df2f0e0259744f64837bf78e20db3849",
    d = "2e7dd5feea4a440a8e4b05bba35984a3",
    e = "fed3d1ed564a4de2a3d1d0747323214f",
    f = "382cb5fa775dbb96a82529011b57c4b0",
    g = "9a3d0cefb70558c0be3a8e2131a4e358",
    h = "e10e8b97e7c9423fa6c9c3e70f56d4c6",
    i = "b11eadb3ef6037ac041eefb4f0b11325",
    j = "b953b215c8d750462b4383a623f35d1a",
}

for _, value in pairs(blocks) do
    block = string.match(filter_args,value)
    if block then
        ngx.exit(ngx.HTTP_FORBIDDEN)
    end
end

-- the request is expired
if ngx.now() - timestamp < -expire_time or ngx.now() - timestamp >= expire_time then
    ngx.status = ngx.HTTP_GONE
    local _now = ngx.now()
    ngx.header.server_time = _now
    ngx.say(_now)
    ngx.exit(ngx.HTTP_OK)
end


-- generate signature
token_string = req_method .. ":" .. ngx.var.uri .. ":" .. filter_args .. ":" .. timestamp .. ":"  .. secret
--ngx.log(ngx.ERR, token_string)
token = ngx.md5(token_string)

-- ngx.log(ngx.ERR, token)

-- Compare sever genned sig(var token) with request sig(request param sig)
if token ~= sig then
    ngx.exit(ngx.HTTP_FORBIDDEN)
else
    return
end
