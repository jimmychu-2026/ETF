// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

(function (modules, entry, mainEntry, parcelRequireName, globalName) {
  /* eslint-disable no-undef */
  var globalObject =
    typeof globalThis !== 'undefined'
      ? globalThis
      : typeof self !== 'undefined'
      ? self
      : typeof window !== 'undefined'
      ? window
      : typeof global !== 'undefined'
      ? global
      : {};
  /* eslint-enable no-undef */

  // Save the require from previous bundle to this closure if any
  var previousRequire =
    typeof globalObject[parcelRequireName] === 'function' &&
    globalObject[parcelRequireName];

  var cache = previousRequire.cache || {};
  // Do not use `require` to prevent Webpack from trying to bundle this call
  var nodeRequire =
    typeof module !== 'undefined' &&
    typeof module.require === 'function' &&
    module.require.bind(module);

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire =
          typeof globalObject[parcelRequireName] === 'function' &&
          globalObject[parcelRequireName];
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error("Cannot find module '" + name + "'");
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = (cache[name] = new newRequire.Module(name));

      modules[name][0].call(
        module.exports,
        localRequire,
        module,
        module.exports,
        this
      );
    }

    return cache[name].exports;

    function localRequire(x) {
      var res = localRequire.resolve(x);
      return res === false ? {} : newRequire(res);
    }

    function resolve(x) {
      var id = modules[name][1][x];
      return id != null ? id : x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [
      function (require, module) {
        module.exports = exports;
      },
      {},
    ];
  };

  Object.defineProperty(newRequire, 'root', {
    get: function () {
      return globalObject[parcelRequireName];
    },
  });

  globalObject[parcelRequireName] = newRequire;

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (mainEntry) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(mainEntry);

    // CommonJS
    if (typeof exports === 'object' && typeof module !== 'undefined') {
      module.exports = mainExports;

      // RequireJS
    } else if (typeof define === 'function' && define.amd) {
      define(function () {
        return mainExports;
      });

      // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }
})({"dYU5o":[function(require,module,exports) {
/* eslint-disable prettier/prettier */ var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
var _factory = require("./_util/factory");
var _api = require("./_util/api");
var _includeTemplate = require("./_util/include_template");
var _includeTemplateDefault = parcelHelpers.interopDefault(_includeTemplate);
const $ = window.$;
const templateName = $("body").data("template");
(0, _includeTemplateDefault.default)[templateName]().then(()=>{
    // $('.datepicker').datePicker({
    //   maxDate: new Date()
    // })
    $(".datepicker").datePicker();
    window.PetiteVue.createApp({
        route: (0, _factory.route),
        store: (0, _factory.store),
        tabs: null,
        current: null,
        remark: null,
        editer: null,
        adBanner: null,
        fundList: null,
        etfPcf: null,
        rate: null,
        isTableHide: true,
        elem: {
            search: {
                fundID: null,
                date: null
            }
        },
        toCurrency: (0, _factory.toCurrency),
        devRoute: (0, _factory.devRoute),
        hrefTarget: (0, _factory.hrefTarget),
        hrefToDevRoute: (0, _factory.hrefToDevRoute),
        editorAddUTM: (0, _factory.editorAddUTM),
        devImage: (0, _factory.devImage),
        onBindUTM: (0, _factory.onBindUTM),
        tabSelected (index) {
            const vm = this;
            return new RegExp(vm.route.params.id).test(vm.tabs[index].route) ? {
                "aria-selected": true
            } : "";
        },
        isChecked (fundID) {
            const vm = this;
            return fundID === vm.current ? {
                "selected": true
            } : null;
        },
        async fetchFundData () {
            const vm = this;
            await (0, _api.getFund)(`fundId=${vm.current}`).then((res)=>{
                const { result  } = res;
                if (result && result.length !== 0) {
                    vm.remark = result[0].ec412;
                    vm.editer = result[0].etf012;
                }
            });
        },
        getFrontWithQuery () {
            const vm = this;
            const fundID = vm.elem.search.fundID.value;
            const date = vm.elem.search.date.value.replace(/\//g, "");
            const searchParam = `fundID=${fundID}&pcfDate=${date}`;
            (0, _factory.store).isLoaded = false;
            (0, _api.getETFPcf)(searchParam).then((res)=>{
                const { result  } = res;
                if (result) {
                    vm.etfPcf = result[0];
                    vm.rate = result[0].rate;
                }
                vm.$nextTick(()=>{
                    (0, _factory.store).isLoaded = true;
                });
            });
            if (vm.current !== fundID) {
                vm.current = fundID;
                vm.fetchFundData();
            }
        },
        showMore () {
            const vm = this;
            vm.isTableHide = false;
        },
        async apiFundList () {
            const vm = this;
            await (0, _api.getFundList)(`ec001=3`).then((res)=>{
                const { result  } = res;
                if (result.length) {
                    vm.fundList = result;
                    vm.current = result[0].fundID;
                }
            });
        },
        async apiETFPcf () {
            const vm = this;
            await (0, _api.getETFPcf)(`fundID=${vm.current}&pcfDate=${vm.elem.search.date.value}`).then((res)=>{
                const { result  } = res;
                if (result) {
                    vm.etfPcf = result[0];
                    vm.rate = result[0].rate;
                }
            });
        },
        async apiAd () {
            const vm = this;
            await (0, _api.getAd)("r=ETFbanner").then((res)=>{
                const { result  } = res;
                if (result && result.length) vm.adBanner = result.slice(0, 2);
            });
        },
        mounted () {
            const vm = this;
            (0, _factory.store).floating.smartBot.onGetMessage();
            (0, _factory.store).floating.smartBot.onRemoveMessage();
            (0, _factory.store).getCommonData(async (guid)=>{
                vm.elem = {
                    search: {
                        fundID: vm.$refs.fundID,
                        date: vm.$refs.date
                    }
                };
                vm.tabs = (0, _factory.generateTabs)("tabs");
                await (0, _factory.store).awaitAllApi([
                    // 取得全站公告
                    (0, _factory.store).getAnnouncement(),
                    vm.fetchFundData(),
                    vm.apiAd(),
                    await vm.apiFundList(),
                    vm.apiETFPcf()
                ]);
                (0, _factory.store).isLoaded = true;
                (0, _factory.store).openAnnouncement();
                window.inputTextFocus();
                window.inputSelect();
                vm.$nextTick(()=>{
                    (0, _factory.finishedApiCall)();
                });
            });
        }
    }).mount("#app");
});

},{"./_util/factory":"83jkO","./_util/api":"keS8U","./_util/include_template":"aZLeu","@parcel/transformer-js/src/esmodule-helpers.js":"4QKYj"}],"aZLeu":[function(require,module,exports) {
/* eslint-disable prettier/prettier */ var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
parcelHelpers.export(exports, "aboutCsr", ()=>aboutCsr);
parcelHelpers.export(exports, "aboutGlory", ()=>aboutGlory);
parcelHelpers.export(exports, "aboutHistory", ()=>aboutHistory);
parcelHelpers.export(exports, "aboutJobs", ()=>aboutJobs);
parcelHelpers.export(exports, "aboutLocations", ()=>aboutLocations);
parcelHelpers.export(exports, "announce", ()=>announce);
parcelHelpers.export(exports, "ETFAnnoucementArticle", ()=>ETFAnnoucementArticle);
parcelHelpers.export(exports, "ETFAnnoucementList", ()=>ETFAnnoucementList);
parcelHelpers.export(exports, "ETFCalendar", ()=>ETFCalendar);
parcelHelpers.export(exports, "ETFDifferentPop", ()=>ETFDifferentPop);
parcelHelpers.export(exports, "ETFDifferent", ()=>ETFDifferent);
parcelHelpers.export(exports, "ETFScale", ()=>ETFScale);
parcelHelpers.export(exports, "ETFValue", ()=>ETFValue);
parcelHelpers.export(exports, "ETFDetail", ()=>ETFDetail);
parcelHelpers.export(exports, "ETFHistory", ()=>ETFHistory);
parcelHelpers.export(exports, "ETFList", ()=>ETFList);
parcelHelpers.export(exports, "ETFListRow", ()=>ETFListRow);
parcelHelpers.export(exports, "ETFHome", ()=>ETFHome);
parcelHelpers.export(exports, "ETFTradeList", ()=>ETFTradeList);
parcelHelpers.export(exports, "ETFPortfolio", ()=>ETFPortfolio);
parcelHelpers.export(exports, "fundsCalendar", ()=>fundsCalendar);
parcelHelpers.export(exports, "fundsHistory", ()=>fundsHistory);
parcelHelpers.export(exports, "fundsCompare", ()=>fundsCompare);
parcelHelpers.export(exports, "fundsData", ()=>fundsData);
parcelHelpers.export(exports, "fundsDetail", ()=>fundsDetail);
parcelHelpers.export(exports, "fundsList", ()=>fundsList);
parcelHelpers.export(exports, "fundsListRow", ()=>fundsListRow);
parcelHelpers.export(exports, "fundsOffer", ()=>fundsOffer);
parcelHelpers.export(exports, "insightsArticleList", ()=>insightsArticleList);
parcelHelpers.export(exports, "insightsContent", ()=>insightsContent);
parcelHelpers.export(exports, "insightsTagResult", ()=>insightsTagResult);
parcelHelpers.export(exports, "investmentAnnounce", ()=>investmentAnnounce);
parcelHelpers.export(exports, "investmentMeetingVotereport", ()=>investmentMeetingVotereport);
parcelHelpers.export(exports, "investmentPolicy", ()=>investmentPolicy);
parcelHelpers.export(exports, "investmentReport", ()=>investmentReport);
parcelHelpers.export(exports, "investmentRecord", ()=>investmentRecord);
parcelHelpers.export(exports, "invMethodComplexCaculate", ()=>invMethodComplexCaculate);
parcelHelpers.export(exports, "invMethodComplexContent", ()=>invMethodComplexContent);
parcelHelpers.export(exports, "invMethodRetireCaculate", ()=>invMethodRetireCaculate);
parcelHelpers.export(exports, "invMethodRetireContent", ()=>invMethodRetireContent);
parcelHelpers.export(exports, "invMethodRobotIntro1Content", ()=>invMethodRobotIntro1Content);
parcelHelpers.export(exports, "invMethodRobotIntro2Content", ()=>invMethodRobotIntro2Content);
parcelHelpers.export(exports, "invMethodTimingCaculate", ()=>invMethodTimingCaculate);
parcelHelpers.export(exports, "invMethodTimingContent", ()=>invMethodTimingContent);
parcelHelpers.export(exports, "retirementArticleList", ()=>retirementArticleList);
parcelHelpers.export(exports, "retirementContent", ()=>retirementContent);
parcelHelpers.export(exports, "retirementCaculate", ()=>retirementCaculate);
parcelHelpers.export(exports, "retirementHome", ()=>retirementHome);
parcelHelpers.export(exports, "servicesPocketArticle", ()=>servicesPocketArticle);
parcelHelpers.export(exports, "servicesPocketFunds", ()=>servicesPocketFunds);
parcelHelpers.export(exports, "servicesPocketRetirement", ()=>servicesPocketRetirement);
parcelHelpers.export(exports, "servicesAccountStep", ()=>servicesAccountStep);
parcelHelpers.export(exports, "servicesAccount", ()=>servicesAccount);
parcelHelpers.export(exports, "servicesCampaign", ()=>servicesCampaign);
parcelHelpers.export(exports, "servicesChatbot", ()=>servicesChatbot);
parcelHelpers.export(exports, "servicesContact", ()=>servicesContact);
parcelHelpers.export(exports, "servicesContentNews", ()=>servicesContentNews);
parcelHelpers.export(exports, "servicesDocument", ()=>servicesDocument);
parcelHelpers.export(exports, "servicesFaq", ()=>servicesFaq);
parcelHelpers.export(exports, "servicesInterestNews", ()=>servicesInterestNews);
parcelHelpers.export(exports, "servicesNewsList", ()=>servicesNewsList);
parcelHelpers.export(exports, "ESGResponsibility", ()=>ESGResponsibility);
parcelHelpers.export(exports, "ESGClimate", ()=>ESGClimate);
parcelHelpers.export(exports, "ESGCompany", ()=>ESGCompany);
parcelHelpers.export(exports, "ESGShareholder", ()=>ESGShareholder);
parcelHelpers.export(exports, "ESGOperating", ()=>ESGOperating);
parcelHelpers.export(exports, "ESGRelation", ()=>ESGRelation);
parcelHelpers.export(exports, "index", ()=>index);
parcelHelpers.export(exports, "noPage", ()=>noPage);
parcelHelpers.export(exports, "login", ()=>login);
const templateRequest = {
    get (path) {
        return fetch(`/_template/${path}?${+new Date()}`, {
            credentials: "include",
            mode: "cors",
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        }).then((res)=>res.text()).then((res)=>{
            const body = new DOMParser().parseFromString(res, "text/html").body;
            document.body.innerHTML = body.innerHTML;
            return document.body;
        });
    }
};
const aboutCsr = ()=>templateRequest.get("about_fhtrust/csr.html");
const aboutGlory = ()=>templateRequest.get("about_fhtrust/glory.html");
const aboutHistory = ()=>templateRequest.get("about_fhtrust/history.html");
const aboutJobs = ()=>templateRequest.get("about_fhtrust/jobs.html");
const aboutLocations = ()=>templateRequest.get("about_fhtrust/locations.html");
const announce = ()=>templateRequest.get("announce/text.html");
const ETFAnnoucementArticle = ()=>templateRequest.get("ETF/annoucement_article.html");
const ETFAnnoucementList = ()=>templateRequest.get("ETF/annoucement_list.html");
const ETFCalendar = ()=>templateRequest.get("ETF/etf_calendar.html");
const ETFDifferentPop = ()=>templateRequest.get("ETF/etf_data_different-pop.html");
const ETFDifferent = ()=>templateRequest.get("ETF/etf_data_different.html");
const ETFScale = ()=>templateRequest.get("ETF/etf_data_scale.html");
const ETFValue = ()=>templateRequest.get("ETF/etf_data_value.html");
const ETFDetail = ()=>templateRequest.get("ETF/etf_detail.html");
const ETFHistory = ()=>templateRequest.get("ETF/etf_history.html");
const ETFList = ()=>templateRequest.get("ETF/etf_list.html");
const ETFListRow = ()=>templateRequest.get("ETF/etf_list_row.html");
const ETFHome = ()=>templateRequest.get("ETF/index.html");
const ETFTradeList = ()=>templateRequest.get("ETF/trade_list.html");
const ETFPortfolio = ()=>templateRequest.get("ETF/portfolio.html");
const fundsCalendar = ()=>templateRequest.get("funds/funds_calendar.html");
const fundsHistory = ()=>templateRequest.get("funds/funds_history.html");
const fundsCompare = ()=>templateRequest.get("funds/funds_compare.html");
const fundsData = ()=>templateRequest.get("funds/funds_data.html");
const fundsDetail = ()=>templateRequest.get("funds/funds_detail.html");
const fundsList = ()=>templateRequest.get("funds/funds_list.html");
const fundsListRow = ()=>templateRequest.get("funds/funds_list_row.html");
const fundsOffer = ()=>templateRequest.get("funds/offer.html");
const insightsArticleList = ()=>templateRequest.get("insights_list/article_list.html");
const insightsContent = ()=>templateRequest.get("insights_list/content_insights.html");
const insightsTagResult = ()=>templateRequest.get("insights_list/tag-result.html");
const investmentAnnounce = ()=>templateRequest.get("investment_stewardship/announce.html");
const investmentMeetingVotereport = ()=>templateRequest.get("investment_stewardship/meeting_votereport.html");
const investmentPolicy = ()=>templateRequest.get("investment_stewardship/policy.html");
const investmentReport = ()=>templateRequest.get("investment_stewardship/report.html");
const investmentRecord = ()=>templateRequest.get("investment_stewardship/record.html");
const invMethodComplexCaculate = ()=>templateRequest.get("InvMethod/complex_intro/caculate.html");
const invMethodComplexContent = ()=>templateRequest.get("InvMethod/complex_intro/content_investment.html");
const invMethodRetireCaculate = ()=>templateRequest.get("InvMethod/retire_concept/content_caculate.html");
const invMethodRetireContent = ()=>templateRequest.get("InvMethod/retire_concept/content_investment.html");
const invMethodRobotIntro1Content = ()=>templateRequest.get("InvMethod/robot_intro_1/content_investment.html");
const invMethodRobotIntro2Content = ()=>templateRequest.get("InvMethod/robot_intro_2/content_investment.html");
const invMethodTimingCaculate = ()=>templateRequest.get("InvMethod/timing_method/caculate.html");
const invMethodTimingContent = ()=>templateRequest.get("InvMethod/timing_method/content_investment.html");
const retirementArticleList = ()=>templateRequest.get("retirement/article_list.html");
const retirementContent = ()=>templateRequest.get("retirement/content_insights.html");
const retirementCaculate = ()=>templateRequest.get("retirement/retirement_caculate.html");
const retirementHome = ()=>templateRequest.get("retirement/retirement_home.html");
const servicesPocketArticle = ()=>templateRequest.get("services/pocket/article.html");
const servicesPocketFunds = ()=>templateRequest.get("services/pocket/funds.html");
const servicesPocketRetirement = ()=>templateRequest.get("services/pocket/retirement.html");
const servicesAccountStep = ()=>templateRequest.get("services/account_step.html");
const servicesAccount = ()=>templateRequest.get("services/account.html");
const servicesCampaign = ()=>templateRequest.get("services/campaign.html");
const servicesChatbot = ()=>templateRequest.get("services/chatbot.html");
const servicesContact = ()=>templateRequest.get("services/contact_us.html");
const servicesContentNews = ()=>templateRequest.get("services/content_news.html");
const servicesDocument = ()=>templateRequest.get("services/document.html");
const servicesFaq = ()=>templateRequest.get("services/faq.html");
const servicesInterestNews = ()=>templateRequest.get("services/interest_news.html");
const servicesNewsList = ()=>templateRequest.get("services/news_list.html");
const ESGResponsibility = ()=>templateRequest.get("ESG/responsibility.html");
const ESGClimate = ()=>templateRequest.get("ESG/climate.html");
const ESGCompany = ()=>templateRequest.get("ESG/company.html");
const ESGShareholder = ()=>templateRequest.get("ESG/shareholder.html");
const ESGOperating = ()=>templateRequest.get("ESG/operating.html");
const ESGRelation = ()=>templateRequest.get("ESG/relation.html");
const index = ()=>templateRequest.get("index.html");
const noPage = ()=>templateRequest.get("404.html");
const login = ()=>templateRequest.get("login.html");
exports.default = {
    aboutCsr,
    aboutGlory,
    aboutHistory,
    aboutJobs,
    aboutLocations,
    announce,
    ETFAnnoucementArticle,
    ETFAnnoucementList,
    ETFCalendar,
    ETFDifferentPop,
    ETFDifferent,
    ETFScale,
    ETFValue,
    ETFDetail,
    ETFHistory,
    ETFList,
    ETFListRow,
    ETFHome,
    ETFTradeList,
    ETFPortfolio,
    fundsCalendar,
    fundsHistory,
    fundsCompare,
    fundsData,
    fundsDetail,
    fundsList,
    fundsListRow,
    fundsOffer,
    insightsArticleList,
    insightsContent,
    insightsTagResult,
    investmentAnnounce,
    investmentMeetingVotereport,
    investmentPolicy,
    investmentReport,
    investmentRecord,
    invMethodComplexCaculate,
    invMethodComplexContent,
    invMethodRetireCaculate,
    invMethodRetireContent,
    invMethodRobotIntro1Content,
    invMethodRobotIntro2Content,
    invMethodTimingCaculate,
    invMethodTimingContent,
    retirementArticleList,
    retirementContent,
    retirementCaculate,
    retirementHome,
    servicesPocketArticle,
    servicesPocketFunds,
    servicesPocketRetirement,
    servicesAccountStep,
    servicesAccount,
    servicesCampaign,
    servicesChatbot,
    servicesContact,
    servicesContentNews,
    servicesDocument,
    servicesFaq,
    servicesInterestNews,
    servicesNewsList,
    ESGResponsibility,
    ESGClimate,
    ESGCompany,
    ESGShareholder,
    ESGOperating,
    ESGRelation,
    index,
    noPage,
    login
};

},{"@parcel/transformer-js/src/esmodule-helpers.js":"4QKYj"}]},["dYU5o"], "dYU5o", "parcelRequiref9f3")

