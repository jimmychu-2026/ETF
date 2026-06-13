/// <reference path="jquery.min.js" />

function mobileCheck() {
	const userAgent = navigator.userAgent;
	const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(userAgent);
	return isMobile;
}

function elementResizeObserver(element, callback) {
	if (element) {
		const resizeObserver = new ResizeObserver(callback);
		resizeObserver.observe(element);
	}
}

/**
 * 我的最愛按鈕點擊互動
 * @param {function} callback - 按下加入最愛按鈕後要執行的函式
 */
$.favoriteToggle = {
	clicked($this, url) {
		const targetType = $this.children().is('i') ? 'css' : 'svg';
		const state = $this.find('.icon').attr('data-look') == 'favorite' || $this.find('use').attr('xlink:href') == '#icon-favorite' || $this.data('favorite-retire') ? 'favorite-actived' : 'favorite';
		const callBackState = state === 'favorite-actived' ? 'add' : 'remove';
		const message = {
			add: {
				text: {
					heading: '已成功加入我的最愛',
					btn: '前往查看'
				},
				url: url
			},
			remove: {
				text: {
					heading: '已取消我的最愛'
				}
			}
		};
		
		// console.log({ state, targetType });

		if (targetType == 'css') {
			$this
				.find('.icon')
				.attr('data-look', state)
				.attr('data-color', callBackState == 'add' ? 'red' : 'black');
		}

		if (targetType == 'svg') {
			$this
				.attr('data-color', callBackState == 'add' ? 'red' : 'black')
				.find('use')
				.attr('xlink:href', `#icon-${state}`);
		}
		
		$.message(message[callBackState]);
	}
}

/**
 *
 * @param {Function} callback - 點擊按鈕後要做的動作\
 * 參數 - 點擊的按鈕 {jQuery Object}\
 */
$.fn.removeTag = function (callback) {
	$(this).one('click', function () {
		$(this).closest('.tag').remove();

		if (typeof callback === 'function') {
			callback($(this));
		}
	});

	return this;
};

// resize
function fundCardToggle(open) {
	let prevWindowWidth = 0;
	function resize(entries) {
		const breakpoint = 905;
		entries.forEach((entry) => {
			const windowWidth = $(window).outerWidth();
			const isResize = prevWindowWidth != windowWidth;
			const isMediumLayout = windowWidth > breakpoint;

			requestAnimationFrame(() => {
				const $details = $('.fundRelative-toggleSon').closest('details');

				if (isResize) {
					if (isMediumLayout) {
						$details.attr('open', true);
					} else {
						if (!open) {
							$details.removeAttr('open');
						} else {
							$details.attr('open', true);
						}
					}
				}
				prevWindowWidth = windowWidth;
			});
		});
	}

	elementResizeObserver($('body')[0], resize);
}

function kvBannerSlider() {
	const kvBannerSlider = tns({
		container: '.kvBannerSlider-container',
		mode: 'gallery',
		items: 1,
		autoplay: true,
		autoplayHoverPause: true,
		autoplayButtonOutput: false,
		loop: true,
		speed: 1000,
		swipeAngle: 12.5,
		preventActionWhenRunning: false,
		animateIn: 'kvBannerIn',
		animateOut: 'kvBannerOut',
		navPosition: 'bottom',
		controlsPosition: 'bottom',
		autoplayPosition: 'bottom',
		onInit: () => {
			$('.tns-nav, .tns-controls').wrapAll("<div class='roundedDotTheme-controls' /><div class='roundedDotTheme-controlsContainer' />");
		}
	});
}

function sliderNavAction(sliderContainer, sliderID) {
	const $nav = $(sliderContainer).closest('.roundedSolidTheme').find('.tns-nav');
	let navPrevIndex, navCurrentIndex;

	const actions = {
		transitionStart: (info, eventName) => {
			const prevIndex = info.indexCached;
			const currentIndex = info.index;
			const direction = prevIndex > currentIndex ? 'prev' : 'next';
			const $controlActive = $nav.find('.tns-nav-active');
			navCurrentIndex = $controlActive.index();
			const controlSizeLess = (direction == 'next' && navPrevIndex == navCurrentIndex) || (direction == 'prev' && currentIndex != navCurrentIndex);

			// console.log('transitionStart');
			// console.log({ controlSizeLess, direction });

			$nav.addClass(`tns-nav-transition tns-nav-${direction}-start tns-nav-${direction}-end`);

			// if (controlSizeLess) {
			// 	$nav.addClass('tns-control-transition');
			// } else {
			// 	$nav.removeClass('tns-control-transition');
			// }
		},
		transitionEnd: (info, eventName) => {
			const prevIndex = info.indexCached;
			const currentIndex = info.index;
			const direction = prevIndex > currentIndex ? 'prev' : 'next';

			// console.log('transitionEnd');
			// console.log({ direction });
			$nav.removeClass(`tns-nav-transition tns-nav-${direction}-start tns-nav-${direction}-end`);
		},
		control: function () {
			const direction = $(this).attr('data-controls');
			navPrevIndex = $nav.find('.tns-nav-active').index();

			// console.log('control');
			// console.log({ direction });

			$nav.addClass(`tns-nav-transition tns-nav-${direction}-start tns-nav-${direction}-end`);
		}
	};

	$(sliderContainer).closest('.roundedSolidTheme').find('[data-controls]').on('click', actions.control);
	sliderID.events.on('transitionStart', actions.transitionStart);
	sliderID.events.on('transitionEnd', actions.transitionEnd);
}

// resize
function mediaCardSlider(options) {
	const $mediaCardSlider = $('.mediaCardSlider-container').filter((index, element) => {
		return $(element).find('[data-layout]').length == 0;
	});
	const $mediaCardRowSlider = $('.mediaCardSlider-container').filter((index, element) => {
		return $(element).find('[data-layout]').length > 0;
	});
	const hasMediaCardSlider = $mediaCardSlider.length > 0;
	const hasMediaCardRowSlider = $mediaCardRowSlider.length > 0;

	if (hasMediaCardSlider) {
		const mediaCardSliders = $mediaCardSlider.map((index, element) => 'mediaCardSlider' + index + 1).get();

		$mediaCardSlider.each(function (index, element) {
			const slider = {
				container: element,
				items: 2,
				loop: false,
				controlsPosition: 'bottom',
				nav: false,
				// navPosition: 'bottom',
				swipeAngle: 45,
				responsive: {
					905: {
						items: 4
					}
				}
			};
			const settings = options && options.slider ? Object.assign(slider, options.slider) : slider;

			mediaCardSliders[index] = tns(settings);

			sliderNavAction(element, mediaCardSliders[index]);
		});
	}

	if (hasMediaCardRowSlider) {
		let mediaCardRowSliders = $mediaCardRowSlider.map((index, element) => 'mediaCardRowSlider' + index + 1).get();
		const breakpoint = options && options.breakpoint ? options.breakpoint : 905;
		let isInit = false;

		function rowSlider(entries) {
			entries.forEach((entry) => {
				const windowWidth = $(window).outerWidth();
				const toggle = {
					action: {
						small: function () {
							// console.log('mediaCardSlider rebuild');
							$('.mediaCard[data-layout="row"]').closest('.mediaCardSlider').removeAttr('data-layout');
							mediaCardRowSliders = mediaCardRowSliders.map((value, index) => {
								value = value.rebuild();
								const info = value.getInfo();

								sliderNavAction(info.container, value);

								return value;
							});

							isInit = true;
						},
						medium: function () {
							// console.log('mediaCardSlider destroy');
							mediaCardRowSliders = mediaCardRowSliders.map((value) => {
								value.destroy();

								return value;
							});

							isInit = false;
							$('.mediaCard[data-layout="row"]').closest('.mediaCardSlider').attr('data-layout', 'row');
						}
					},
					breakpoint: {
						small: windowWidth < breakpoint && !isInit,
						medium: windowWidth >= breakpoint && isInit
					}
				};

				if (toggle.breakpoint.medium) {
					requestAnimationFrame(toggle.action.medium);
				} else if (toggle.breakpoint.small) {
					requestAnimationFrame(toggle.action.small);
				}
			});
		}

		$mediaCardRowSlider.each(function (index, element) {
			const rowSlider = {
				container: element,
				items: 2,
				loop: false,
				controlsPosition: 'bottom',
				nav: false,
				// navPosition: 'bottom',
				swipeAngle: 45,
				onInit: () => {
					isInit = true;
				}
			};
			const settings = options && options.rowSlider ? Object.assign(rowSlider, options.rowSlider) : rowSlider;
			mediaCardRowSliders[index] = tns(settings);

			sliderNavAction(element, mediaCardRowSliders[index]);
		});
		elementResizeObserver($('body')[0], rowSlider);
	}
}

function tabNav(callback) {
	const $tab = $('.tab');
	const hash = window.location.hash
	const search = window.location.search && /tab=/.test(window.location.search)
									? /tab\=([^?&#]*)/.exec(window.location.search)[1]
									: null

	$tab.each((index) => {
		const $tabItem = $tab.eq(index);
		const $panel = $tabItem.attr('aria-controls');
		
		if ((search && new RegExp(search).test($tabItem.attr('href'))) || (hash && $tabItem.attr('href') === hash)) {
			$tabItem.attr('aria-selected', 'true').siblings().removeAttr('aria-selected');

			$(`${$panel}`).removeAttr('hidden').siblings('.tabPanel').attr('hidden', 'true');
		}

		if (search && new RegExp(search).test($tabItem.attr('href'))) {
			if (typeof callback === 'function') {
				requestAnimationFrame(function () {
					callback($(`${$panel}`), $tabItem, index);
				});
			}
		}
	})
	

	$tab.on('click', function (e) {
		const $this = $(this);
		const $panel = $this.attr('aria-controls');
		const index = $(this).index()

		$this.attr('aria-selected', 'true').siblings().removeAttr('aria-selected');
		$(`${$panel}`).removeAttr('hidden').siblings('.tabPanel').attr('hidden', 'true');

		if (typeof callback === 'function' && !search) {
			requestAnimationFrame(function () {
				callback($(`${$panel}`), $this, index);
			});
		}
	});
}

/**
 *
 * @param {Object} configs - 設定tabSlider，請參照[tiny-slider](https://github.com/ganlanyuan/tiny-slider)網站說明\
 * @returns {Object} - 返回tabSlider 可在另外做其他event控制
 * @example
 * tabSlider({
 * 	id:...,
 * 	setting:{
 * 		//...tiny-slider options
 * 	}
 * })
 */
function tabSlider(config) {
	return (config.id = tns({
		loop: false,
		nav: false,
		navPosition: 'bottom',
		...config.setting
	}));
}

function inputSelect(isFilter) {
	const $inputSelect = $('.inputSelect');
	const isMobile = mobileCheck();
	const actions = {
		selectChange: function () {
			const selectValue = $(this).find(':selected').text();
			const $selectDisplay = $(this).closest('.inputSelect').find('.accordion-toggleText');

			$selectDisplay.text(selectValue);
		},
		optionClick: function ($option) {
			const optionsID = $option.attr('for');
			const $inputFilter = $option.parent();
			const $accordion = $option.closest('details');
			const $select = $accordion.next();

			$inputFilter.attr('data-checked', true).siblings().removeAttr('data-checked');
			$select.find(`[data-range="${optionsID}"], [value="${optionsID}"]`).prop('selected', true).siblings().prop('selected', false).parent().trigger('change');
			$accordion.removeAttr('open');
			$('body').off('click.inputSelect');
		},
		openedAccordion: function (event) {
			const $inputSelect = $(this).parent();
			const opened = !$inputSelect.is('[open]');
			const $container = $(this).next()
			const $inputFilters = $container.find('.inputFilter');
			const isPosition = $inputSelect.parent().data('position')
			const position = () => {
				if (isPosition) {
					$container.children().scrollTop(0)

					for (let i = 0; i < $inputFilters.length; i+=1) {
						const $inputFilter = $inputFilters[i];
						
						if ($($inputFilter).attr('data-checked') === 'true') {
							const scrollTop = $($inputFilter).position().top;
	
							$container.children().scrollTop(scrollTop);
						}
					}
				}
			}

			$('.inputSelect details').not($(this).parent()).removeAttr('open');
			$('body').off('click.inputSelect');

			if (opened) {
				requestAnimationFrame(() => {
					actions.blur($inputSelect);
					position()
				});
			}
		},
		init: () => {
			const $inputSelect = $('.inputSelect');
			$inputSelect.each(function () {
				const $selectOption = $(this).find(':selected');
				const optionID = $selectOption.attr('data-range') || $selectOption.val();
				const $select = $(this).find('select');
				const $selectDisplay = $(this).find('.accordion-toggleText');
				const selectValue = $selectOption.text();

				if (!isFilter && isMobile) {
					$selectDisplay.parent().attr('data-mobile', true);
				} else {
					$selectDisplay.parent().removeAttr('data-mobile');
				}

				$(this).find('.inputFilter').attr('data-checked', false);

				if (optionID) {
					$(`[for=${optionID}]`).parent().attr('data-checked', true);
				}

				$selectDisplay.text(selectValue);
				$select.on('change', actions.selectChange);
			});
		},
		blur: function ($openedSelect) {
			$('body').on('click.inputSelect', function (event) {
				event.stopImmediatePropagation();
				const $target = $(event.target);
				const clickedInputSelect = $target.closest('.inputSelect').length > 0;
				const clickedOption = $target.closest('.inputFilter').length > 0;

				if (!clickedInputSelect) {
					$openedSelect.removeAttr('open');
					$('body').off('click.inputSelect');
				}

				if (clickedOption && !isFilter) {
					actions.optionClick($target);
				}
			});
		}
	};

	if (!isFilter) {
		actions.init();
	}
	$inputSelect.each(function () {
		$(this).find('.accordion-toggle').on('click', actions.openedAccordion);
	});
}

/**
 *
 * @param {Function} callback - 選取input後要做的動作\
 * 參數 - 點擊的input {jQuery Object}\
 * 參數 - 是否被選取 {boolean}\
 */
function inputFilter(callback) {
	function FilterChange() {
		const filterChecked = $(this).is(':checked');

		if (filterChecked) {
			$(this).closest('.inputFilter').attr('data-checked', true);
		} else {
			$(this).closest('.inputFilter').removeAttr('data-checked');
		}

		if (typeof callback === 'function') {
			callback($(this), filterChecked);
		}
	}

	inputSelect(true);
	$('.inputFilter .inputCheckbox').on('change', FilterChange);
}

/**
 * @param {Boolean} enterClick - 是否按下Enter鍵後觸發search按鈕的click事件
 * @param {Function} callback - 按下搜尋按鈕後的callback\
 * 參數 - searchButton {jQuery Object}
 */
$.fn.inputSearch = function (enterClick, callback) {
	const $input = this;
	const $clearButton = $input.next().find('.inputTextButton-clear');
	const $searchButton = $input.next().find('.inputTextButton-search');

	function clearKeyword() {
		$input.removeAttr('data-autocomplete').val('');
	}
	function search() {
		const value = $input.val();
		const hasValue = value.length > 0;

		if (typeof callback === 'function' && hasValue) {
			callback($(this));
		}
	}
	function keyInEnter(event) {
		const keyIn = event.key;
		const keyInEnter = keyIn === 'Enter';

		if (keyInEnter) {
			$searchButton.trigger('click');
		}
	}

	$clearButton.on('click', clearKeyword);
	$searchButton.on('click', search);

	if (enterClick) {
		$input.on('keyup', keyInEnter);
	}

	return this;
};

/**
 *
 * @param {Function} searchData - 關鍵字比對邏輯\
 * 參數 - keyword {string}\
 * 回傳 - 比對完的資料 {array}
 * @param {Function} callback - 點選項目後的預設動作
 * 參數 - key {string} 回傳鍵盤操作的鍵值
 * 參數 - searchPanel {jQuery Object}
 * 參數 - selected element {jQuery Object}
 */
$.fn.autocomplete = function (searchData, callback) {
	let scheduledSearch;
	const $searchBar = this;
	const $panel = $searchBar.siblings('.searchPanel').children();

	const inputAction = {
		showPanel: async function (event) {
			$('body').off('click.searchPanel');

			const $input = $(this);
			const $panel = $(this).siblings('.searchPanel').children();
			const keyIn = event.key;
			const keyInUp = keyIn == 'ArrowUp';
			const keyInDown = keyIn == 'ArrowDown';
			const keyInSelect = keyInUp || keyInDown;
			const panelDisplay = $input.attr('data-autocomplete') == 'true';
			const keyword = $input.val();

			if (panelDisplay && keyInSelect) {
				const $focus = $(':focus');
				const isInputFocus = $focus.hasClass('inputText');

				if (isInputFocus) {
					const item = keyInDown ? ':first-child' : ':last-child';
					const value = $panel.children(item).text();
					const id = $panel.children(item).attr('data-id');
					const url = $panel.children(item).attr('data-url');

					if (id) {
						$input.attr({ 'data-id': id });
					}

					if (url) {
						$input.attr({ 'data-url': url });
					}

					$input.val(value);

					requestAnimationFrame(function () {
						$panel.children(item).focus().attr('data-selected', true);
					});
				}
			}

			if (scheduledSearch) return;

			scheduledSearch = true;
			const list = await searchData(keyword);
			const hasList = list.length > 0;

			if (hasList) {
				$input.attr('data-autocomplete', true);
				await searchList.insert(list, $panel);
			} else {
				$input.removeAttr('data-autocomplete');
				searchList.clear($panel);
			}

			scheduledSearch = false;
		},
		unFocus: function (event) {
			const target = $(event.target);
			const targetNotSearch = !target.siblings().hasClass('searchPanel-item') || !target.siblings().has('[type="search"]');

			if (targetNotSearch) {
				$searchBar.removeAttr('data-autocomplete');
			}
		},
		blur: function () {
			$('body').on('click.searchPanel', inputAction.unFocus);
		}
	};
	const searchList = {
		insert: function (list, panelElement) {
			const options = list.map((value, i) => `<li class="searchPanel-item py-2 pl-4 pr-2"${value.autoComplete.url ? ` data-url="${value.autoComplete.url}"` : ''}${value.autoComplete.id ? ` data-id=${value.autoComplete.id}` : ''}${value.autoComplete.ga4Event ? ` ga4-event="${value.autoComplete.ga4Event}" ga4-parameter_1="${value.twNameFull}"` : ''} tabindex="-1">${value.twNameFull}</li>`).join('');
			const listSize = list.length;

			panelElement.html(options);

			for (let i = 0; i < $(panelElement).find('.searchPanel-item').length; i+=1) {
				const $item = $(panelElement).find('.searchPanel-item').eq(i);

				$item.on('click', (e) => {
					const $this = $(e.currentTarget)
					const text = $this.text()

					if ($this.data('url')) {
						window.location.href = $this.data('url')
					} else {
						$($searchBar).val(text)
					}
				})
			}
		},
		clear: function (panelElement) {
			panelElement.empty();
		}
	};
	const searchPanel = {
		choice: function (event) {
			const $panel = $(this);
			const $option = $(event.target);
			const $input = $panel.siblings('[type="search"]');
			const keyIn = event.key;
			const keyInEnter = keyIn == 'Enter';
			const keyInUp = keyIn == 'ArrowUp';
			const keyInDown = keyIn == 'ArrowDown';
			const keyInSelect = keyInUp || keyInDown;

			if (keyInSelect) {
				const optionSize = $panel.children().length;
				const selectedIndex = $option.index();
				const goLast = selectedIndex == 0 && keyInUp;
				const goFirst = selectedIndex == optionSize - 1 && keyInDown;
				const goNext = keyInDown;
				const goPrev = keyInUp;
				let id, url, value;

				if (goNext) {
					const item = goFirst ? ':first-child' : `:eq(${selectedIndex + 1})`;

					value = $panel.children(item).text();
					id = $panel.children(item).attr('data-id');
					url = $panel.children(item).attr('data-url');

					$panel.children(item).focus().attr('data-selected', true).siblings().removeAttr('data-selected');
				}

				if (goPrev) {
					const item = goLast ? ':last-child' : `:eq(${selectedIndex - 1})`;
					value = $panel.children(item).text();
					id = $panel.children(item).attr('data-id');
					url = $panel.children(item).attr('data-url');

					$panel.children(item).focus().attr('data-selected', true).siblings().removeAttr('data-selected');
				}

				if (id) {
					$input.attr({ 'data-id': id });
				}

				if (url) {
					$input.attr({ 'data-url': url });
				}

				$searchBar.val(value);
			}

			if (keyInEnter && typeof callback === 'function') {
				$panel.trigger('click', ['enter']);
			}
		},
		selected: function (event, key) {
			if (typeof callback === 'function') {
				callback(key, $(this), $(event.target));
			}
		}
	};

	$searchBar.inputSearch(false);

	$searchBar.on('keyup focus', inputAction.showPanel).on('blur', inputAction.blur);
	$panel.on('keyup', searchPanel.choice).on('click', searchPanel.selected);

	return this;
};

$.fn.rangeDatePicker = function (options) {
	let fromPicker, toPicker;
	const $floatNav = $('.floatNav');
	const defaults = {
		yearRange: 1,
		selectAssociation: false,
		allowInput: true,
		disableMobile: true,
		dateFormat: 'Y/m/d',
		clickOpens: false,
		locale: {
			firstDayOfWeek: 1,
			weekdays: {
				shorthand: ['日', '一', '二', '三', '四', '五', '六'],
				longhand: ['週日', '週一', '週二', '週三', '週四', '週五', '週六']
			},
			months: {
				shorthand: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
				longhand: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
			},
			rangeSeparator: ' 至 ',
			weekAbbreviation: '週',
			scrollTitle: '滾動切換',
			toggleTitle: '點擊切換 12/24 小時時制'
		},
		onOpen: function (selectedDates, dateStr, instance) {
			const $input = $(instance.input);
			const minDate = $($input.parent().parent().find('div')[0]).find('[data-range]').val() || $input.parent().find('[data-range="form"]').val()
			const maxDate = $($input.parent().parent().find('div')[1]).find('[data-range]').val() || $input.parent().find('[data-range="to"]').val()
			const timeout = setTimeout(() => {
				window.clearTimeout(timeout)
				fromPicker.setDate(minDate, true);
				toPicker.setDate(maxDate, true);
			}, 0);
			fromPicker.set('maxDate', new Date(maxDate));
			toPicker.set('minDate', new Date(minDate));

			
			$('body').attr('data-noScroll', true);
			$input.parent().attr('data-datePicker', true);
		},
		onClose: function (selectedDates, dateStr, instance) {
			const $input = $(instance.input);
			// const fromDate = fromPicker.selectedDates[0];

			// toPicker.set('minDate', fromDate);
			$input.parent().removeAttr('data-datePicker');
			$('body').removeAttr('data-noScroll');
			$input.trigger('blur');
			$floatNav.removeAttr('style');
		}
	};
	const settings = $.extend({}, defaults, options);

	const date = {
		today: new Date(),
		maxDate: {
			from: function () {
				const maxDate = new Date().setDate(new Date().getDate() - 1);
				return new Date(maxDate);
			}
		},
		prevYearToday: function () {
			const prevYear = new Date().setFullYear(new Date().getFullYear() - settings.yearRange);
			return new Date(prevYear);
		}
	};

	const datePickerConfig = {
		from: {
			defaultDate: settings.from ? settings.from.defaultDate ?? date.prevYearToday() : date.prevYearToday(),
			minDate: settings.from
									? (settings.from.minDate && !isNaN(+new Date(settings.from.minDate)))
										? settings.from.minDate
										: '1998/01/01'
									: '1998/01/01',
			maxDate: settings.from ? settings.from.maxDate ?? date.today : date.today,
			...settings
		},
		to: {
			defaultDate: settings.to ? settings.to.defaultDate ?? date.today : date.today,
			minDate: settings.to
								? (settings.to.minDate && !isNaN(+new Date(settings.to.minDate)))
									? settings.to.minDate
									: null
								: date.prevYearToday(),
			maxDate: settings.to ? settings.to.maxDate ?? date.today : date.today,
			...settings
		}
	};

	fromPicker = flatpickr($(this).find('[data-range="from"]')[0], datePickerConfig.from);
	toPicker = flatpickr($(this).find('[data-range="to"]')[0], datePickerConfig.to);
	const fromDate = fromPicker.selectedDates[0];
	const toDate = toPicker.selectedDates[0];
	
	// console.log(toDate)

	if (settings.selectAssociation) {
		// const $select = this.find('select');
		// function selectActions() {
		// 	const time = $(this).children(':selected').val();
		// 	const range = $(this).children(':selected').data('range');
		// 	const selectedFrom =
		// 		range == 'yearNow'
		// 								? `${new Date(toDate).getFullYear()}/1/1`
		// 								: range != 'all'
		// 									? new Date(toDate).setMonth(toDate.getMonth() + parseInt(time))
		// 									: time;
		// 	const selectedTo = new Date(toDate);

			

		// 	// fromPicker.setDate(selectedFrom, true);
		// 	// toPicker.set('minDate', fromPicker.selectedDates[0]);
		// 	// setTimeout(() => {
		// 	// 	toPicker.setDate(selectedTo, true);
		// 	// }, 100);
		// }

		inputSelect();

		// $select.on('change', selectActions).trigger('change');
	}
};

$.fn.datePicker = function (options) {
	const $floatNav = $('.floatNav');
	let datePicker;
	const defaults = {
		disableMobile: true,
		dateFormat: 'Y/m/d',
		clickOpens: false,
		locale: {
			firstDayOfWeek: 1,
			weekdays: {
				shorthand: ['日', '一', '二', '三', '四', '五', '六'],
				longhand: ['週日', '週一', '週二', '週三', '週四', '週五', '週六']
			},
			months: {
				shorthand: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
				longhand: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
			},
			rangeSeparator: ' 至 ',
			weekAbbreviation: '週',
			scrollTitle: '滾動切換',
			toggleTitle: '點擊切換 12/24 小時時制'
		},
		defaultDate: $(this).data('date') || new Date(),
		minDate: $(this).data('min') || null,
		maxDate: $(this).data('max') || null,
		onOpen: function (selectedDates, dateStr, instance) {
			const $input = $(instance.input);

			$('body').attr('data-noScroll', true);
			$input.parent().attr('data-datePicker', true);
		},
		onClose: function (selectedDates, dateStr, instance) {
			const $input = $(instance.input);

			$input.parent().removeAttr('data-datePicker');
			$('body').removeAttr('data-noScroll');
			$input.trigger('blur');
			$floatNav.removeAttr('style');
		}
	};
	const settings = $.extend({}, defaults, options);

	datePicker = flatpickr($(this)[0], settings);
};

// resize
function header() {
	let prevElementWidth = 0;
	const subNavToggle = {
		level1: function (event) {
			event.stopImmediatePropagation();
			const isSmallLayout = $('.header-sideHeader').is(':visible');
			const isSelected = $(this).attr('data-selected') === 'true';

			if (isSmallLayout) {
				// console.log({ isSelected });
				$(this).attr('data-selected', !isSelected);
			}
		},
		level2: function (event) {
			event.stopImmediatePropagation();
			const isSmallLayout = $('.header-sideHeader').is(':visible');
			const goOpen = $(this).children().hasClass('header-toggle--open');

			if (isSmallLayout) {
				$('.header-side').attr('data-open', goOpen);
				$('body').attr('data-noScroll', goOpen);
				$('.header').attr('data-sideNav', goOpen);
			}
		}
	};
	function resize(entries) {
		const breakpoint = 905;
		entries.forEach((entry) => {
			const elementWidth = entry.contentRect.width;
			const isMediumLayout = elementWidth > breakpoint;
			const isResize = prevElementWidth != elementWidth;
			const hasLightbox = $('.lightbox').is('[data-opened="true"]');

			if (isResize) {
				requestAnimationFrame(() => {
					if (isMediumLayout) {
						$('.header-side').removeAttr('data-open');
						$('.header').removeAttr('data-sideNav');
						$('.mainNav-link, .subNav-link').removeAttr('data-selected');
						if (!hasLightbox) {
							$('body').removeAttr('data-noScroll');
						}
					}
				});
				prevElementWidth = elementWidth;
			}
		});
	}

	$('.mainNav-link, .subNav-link[data-subNav="true"]').on('click', subNavToggle.level1);
	$('.header-toggle').on('click', subNavToggle.level2);
	$('.header').on('click', (e) => {
		if ($('.header-sideHeader').is(':hidden') || e.target !== e.delegateTarget) return;
		$('.header-toggle').has('.header-toggle--close').triggerHandler('click');
	});
	elementResizeObserver($('.header')[0], resize);

}

function handleMarquee() {
	const isMarquee = $('.marquee').length > 0;

	if (isMarquee) {
		marquee();
	}
}

function marquee() {
	const marquee = tns({
		container: '.marquee-list',
		items: 1,
		loop: true,
		autoHeight: true,
		autoplay: true,
		autoplayButtonOutput: false,
		axis: 'vertical',
		nav: false,
		controls: false
	});

	function removeMarquee() {
		$('.marquee').remove();
	}

	$('.marquee-closeBtn').one('click', removeMarquee);
}

// resize
function footer() {
	let prevElementWidth = 0;
	function resize(entries) {
		const breakpoint = 905;
		entries.forEach((entry) => {
			const elementWidth = entry.contentRect.width;
			const $accordion = $('.footer-warning');
			const isMediumLayout = elementWidth >= breakpoint;
			const isResize = prevElementWidth != elementWidth;

			if (isResize) {
				requestAnimationFrame(() => {
					if (isMediumLayout) {
						$accordion.attr('open', 'true');
					} else {
						$accordion.removeAttr('open');
					}
				});
				prevElementWidth = elementWidth;
			}
		});
	}

	if($('.footer').length) elementResizeObserver($('.footer')[0], resize);
}

function fundFilterToggle() {
	let prevElementWidth;
	prevElementWidth = 0;
	const actions = {
		toggleFilter: function () {
			const isSelected = $(this).attr('data-selected') === 'true';
			const $filter = $(this).closest('.filter');

			$filter.attr('data-filter', !isSelected);
			$(this).attr('data-selected', !isSelected).parent().siblings().children('.filter-inputToggle').removeAttr('data-selected');

			requestAnimationFrame(function () {
				if (!isSelected) {
					$('body').on('click.fundFilter', function (e) {
						const $target = $(e.target);
						const close = $target.closest('.filter-search, .filter-checkbox').length === 0;
						const searchHasValue = $target.closest('.filter-search').find('.inputTextButton-clear').is(':visible');

						// console.log({ $target, close, searchHasValue });

						if (searchHasValue) {
							$('.inputTextButton-clear').triggerHandler('click');
						}
						if (close) {
							actions.closeFilter();
						}
					});
				} else {
					$('body').off('click.fundFilter');
				}
			});
		},
		closeFilter: function () {
			$('.filter-inputToggle[data-selected=true]').trigger('click');
		},
		windowResize: (entries) => {
			const breakpoint = 905;
			entries.forEach((entry) => {
				const elementWidth = parseInt(entry.contentRect.width);
				const isResize = prevElementWidth != elementWidth && prevElementWidth != 0;
				const isMediumLayout = elementWidth >= breakpoint;

				requestAnimationFrame(function () {
					if (isMediumLayout) {
						$('.filter-inputToggle').removeAttr('data-selected');
						$('.filter').removeAttr('data-filter');
					}
					if (isResize) {
						$('.filter-inputContainer').find('.accordion').removeAttr('open');
					}
					prevElementWidth = elementWidth;
				});
			});
		}
	};

	$('.filter-inputToggle').on('click', actions.toggleFilter);
	$('.btn-filterClose').on('click', actions.closeFilter);
	elementResizeObserver($('.filter')[0], actions.windowResize);
}

/**
 *
 * @param {Number} compareSize - 已經加入比較名單的卡片數量
 */
function FloatFundCompareDisplay(compareSize) {
	const $floatFundCompare = $('.floatFundCompare');
	const $selected = $('.floatFundCompare-selected');
	// const $footerElement = $('.footer')[0];
	const active = compareSize > 0;
	function FloatFundCompareToggle() {
		const $floatFundCompare = $(this).closest('.floatFundCompare');
		const isOpen = $(this).closest('details').attr('open');

		// console.log(0)

		$floatFundCompare.attr('data-open', !isOpen);
	}

	$floatFundCompare.attr('data-active', active);
	if (!active) {
		$floatFundCompare.find('details').removeAttr('open');
		$floatFundCompare.attr('data-open', false);
		// $footerElement.style.setProperty('--floatCompare-height', '0px');
		$('.floatFundCompare-toggle').off('click');
	} else {
		$('.floatFundCompare-toggle').on('click', FloatFundCompareToggle).trigger('click');
		// $footerElement.style.setProperty('--floatCompare-height', '66px');
	}
	$selected.text(compareSize);
}

/**
 *
 * @param {Array} fundData
 * @example
 * [{
 * 	checkedID: 被選取加入比較的checkbox的id {String},
 * 	name: 基金名稱 {String}
 * }]
 */
function FloatFundCompareCardInsert(fundData, callback) {
	const $floatFundCompare = $('.floatFundCompare');

	const cardTemplate = function (name) {
		return `<p>${name}</p>
		<div class="floatFundCompare-delete btnContainer absolute posr-3" data-align="center" data-valign="center">
			<button type="button" class="btn--icon btn-icon" title="刪除"><i class="icon" data-look="close"></i></button>
		</div>`;
	};
	function deleteCard($card) {
		const ID = $card.attr('data-checkboxid');

		$(`${ID}`).prop('checked', false);

		// console.log(callback)

		if(typeof callback === 'function') {
			callback({checkedID: ID});
		}
	}

	

	$.each(fundData, function (i, data) {
		const fundCheckedID = data.checkedID;
		const fundName = data.name;
		const $card = cardTemplate(fundName);

		const $inset = $floatFundCompare.find('.floatFundCompare-card:empty:first');
		$inset.attr('data-checkboxid', fundCheckedID).append($card);
		$inset.FloatFundCompareDeleteCard(deleteCard);
	});
}

/**
 * @param {Function} callback - 刪除基金後的callback
 * 參數 - $('.floatFundCompare-card') 比較名單的基金卡片 {jQuery Object}
 */
$.fn.FloatFundCompareDeleteCard = function (callback) {
	$(this).one('click', function () {
		const $card = $(this).closest('.floatFundCompare-card');
		const checkboxID = $card.attr('data-checkboxid');
		const $tableCard = $(`#${checkboxID}`).closest('.fundListTable-fundCard');
		const selectType = $(`#${checkboxID}`).closest('.btn-compare').is('button') ? 'button' : 'input';

		$card.empty();
		$(`#${checkboxID}`).prop('checked', false);
		if (selectType == 'button') {
			$(`#${checkboxID}`).closest('.btn-compare').attr('data-color', 'black');
		}

		const compareSize = $card.siblings('.floatFundCompare-card:not(:empty)').length;
		$tableCard.removeAttr('data-compare');
		FloatFundCompareDisplay(compareSize);

		if (typeof callback === 'function') {
			callback($card);
		}
	});

	return this;
};

/**
 *
 * @param {Function} selectedCallback - 選取加入比較後的callback\
 * 參數 - 點選加入比較清單後的行為 `add` `remove` `limit`  {String}
 * @param {Function} goPageCallback - 點選前往基金比較後的callback\
 * 點選後不會觸發換頁的行為，待處理好邏輯後在自行觸發
 * 參數 - 基金清單頁的網址 {String}
 */
function compareToggle(selectedCallback, goPageCallback) {
	function clicked() {
		const targetType = $(this).is('button') ? 'button' : 'input';
		const $floatFundCompare = $('.floatFundCompare');
		let selectedSize = $floatFundCompare.find('.floatFundCompare-card:not(:empty)').length;
		const $tableCard = $(this).closest('.fundListTable-fundCard');
		const checkedID = targetType == 'button' ? $(this).find('input').attr('id') : $(this).attr('id');
		const state = targetType == 'button' ? $(this).find('input').is(':checked') : $(this).is(':checked');

		const isLimit = state === true && selectedSize == 3;
		const callBackState = isLimit ? 'limit' : state === true ? 'add' : 'remove';
		const fundData = [
			{
				checkedID: checkedID,
				name: targetType == 'button' ? $(this).closest('.fundState').find('.fundState-name').text() : $(this).closest('.fundListTable-fundCard').find('.fundListTable-fundName').text()
			}
		];
		const message = {
			add: {
				text: {
					heading: '已成功加入基金比較'
				}
			},
			remove: {
				text: {
					heading: '已取消加入基金比較'
				}
			},
			limit: {
				text: {
					heading: '比較最多僅能加入3檔基金，麻煩先取消其他的選擇'
				}
			}
		};

		$.message(message[callBackState]);

		if (callBackState == 'add') {
			if (targetType == 'button') {
				$(this).attr('data-color', 'red');
			}

			$tableCard.attr('data-compare', true);
			FloatFundCompareCardInsert(fundData);
		}

		if (callBackState == 'remove') {
			if (targetType == 'button') {
				$(this).attr('data-color', 'black');
			}

			$tableCard.removeAttr('data-compare');
			$(`[data-checkboxid="${checkedID}"]`).removeAttr('data-checkboxid').empty();
		}

		if (isLimit) {
			$(`#${checkedID}`).prop('checked', false);
		}

		selectedSize = $floatFundCompare.find('.floatFundCompare-card:not(:empty)').length;
		FloatFundCompareDisplay(selectedSize);

		if (typeof selectedCallback === 'function') {
			selectedCallback(callBackState, {
				name: $(this).attr('name'),
				checkedID: $(this).attr('id')
			});
		}
	}
	function checkSize(event) {
		event.preventDefault();
		const url = $(this).attr('href');
		const selectedSize = $(this).parent().siblings('.floatFundCompare-card:not(:empty)').length;
		const isOne = selectedSize == 1;

		if (isOne) {
			$.message({
				text: {
					heading: '麻煩再選擇至少一檔基金，才能進行基金比較'
				}
			});
		} else {
			if (typeof goPageCallback === 'function') {
				goPageCallback(url);
			}
		}
	}

	$('.btn-goCompare').off('click').on('click', checkSize);
	$('.btn-compare').off('change').on('change', clicked);
}

$.message = function (options) {
	let timer = null;
	const defaults = {
		text: {
			heading: '',
			btn: ''
		},
		url: '',
		displayDuration: 2000
	};
	const settings = $.extend({}, defaults, options);

	const template = $(`<section class="dialog" data-type="message">
		<div class="dialog-container">
			<div class="dialog-content">
				<h1 class="dialog-heading color-red-500">${settings.text.heading}</h1>
			</div>
			${
				settings.text.btn
					? `<div class="dialog-btn btnContainer" data-align="center" data-valign="center" data-layout="column">
			<a href="${settings.url}" class="btn--primary" data-size="medium"><span>${settings.text.btn}</span></a>
		</div>
	</div>`
				: ''
		}
	</section>`);
	
	$('.dialog').remove();
	$('body').append(template);
	const $container = template.find('.dialog-container')
	$container.addClass('dialog--add');

	const addDuration = parseFloat($container.css('transition-duration'), 10) * 1000

	$container.stop(true).delay(settings.displayDuration).queue(() => {
		$container.addClass('dialog--remove').stop(true).delay(addDuration).queue(() => {
			template.remove().dequeue();
		}).dequeue()
	})
	// template.off('transitionend').on('transitionend', transition);
};

$.alert = function (options) {
	const defaults = {
		text: {
			heading: '',
			description: '',
			btn: '',
			closeBtn: false,
			btnClass: null,
			descriptionClass: null
		},
		done: $.noop
	};
	const settings = $.extend({}, defaults, options);
	const template = $(`<section class="dialog" data-type="alert">
	<div class="dialog-container">
		<div class="dialog-content">
			${settings.text.closeBtn ? '<div class="dialog-closeBtn top-[20] right-[20] absolute"><button type="button" class="m-0 p-0 border-none bg-transparent w-[20] h-[20] flex items-center justify-center cursor-pointer" title="關閉"><i class="icon" data-look="close"></i></button></div>' : ''}
			<h1 class="dialog-heading color-red-500 text-center">${settings.text.heading}</h1>
			<p${settings.text.descriptionClass ? ` class="${settings.text.descriptionClass}"` : ''}>${settings.text.description}</p>
		</div>
		<div class="dialog-btn btnContainer" data-align="center" data-valign="center" data-layout="column">
			${settings.text.href ? `<a href="${settings.text.href}" class="btn--primary${settings.text.btnClass ? ` ${settings.text.btnClass}` : ''}" data-size="medium"${settings.text.target ? ` target="${settings.text.target} rel="noopener"` : ''}><span>${settings.text.btn}</span></a>` : `<button type="button" class="btn--primary${settings.text.btnClass ? ` ${settings.text.btnClass}` : ''}" data-size="medium"><span>${settings.text.btn}</span></button>`}
		</div>
	</div>
</section>`);

	function closeDialog(event) {
		const $dialog = $(event.currentTarget).closest('.dialog');

		$dialog.remove();

		if (typeof settings.done === 'function') {
			settings.done();
		}
	}

	template.one('click', '.dialog-btn', closeDialog);
	$('body').append(template).addClass('overflow-hidden');
	template.one('click', '.dialog-closeBtn', (e) => {
		const $target = $(e.currentTarget);
		const $dialog = $target.closest('.dialog');
		$dialog.remove();
		$('body').removeClass('overflow-hidden')
	})
};

$.confirm = function (options) {
	const defaults = {
		text: {
			heading: '',
			description: '',
			closeBtn: false,
			btnClass: null,
			doneBtn: '',
			cancelBtn: '',
			descriptionClass: null
		},
		overlayer: false,
		done: $.noop,
		cancel: $.noop
	};
	const settings = $.extend({}, defaults, options);
	const template = $(`<section class="dialog${settings.overlayer ? ' --overlayer' : ''}" data-type="confirm">
	<div class="dialog-container">
		<div class="dialog-content">
			${settings.text.closeBtn ? '<div class="dialog-closeBtn top-[20] right-[20] absolute"><button type="button" class="m-0 p-0 border-none bg-transparent w-[20] h-[20] flex items-center justify-center cursor-pointer" title="關閉"><i class="icon" data-look="close"></i></button></div>' : ''}
			${settings.text.heading ? `<h1 class="dialog-heading color-red-500 text-center">${settings.text.heading}</h1>` : ''}
			<p${settings.text.descriptionClass ? ` class="${settings.text.descriptionClass}"` : ''}>${settings.text.description}</p>
		</div>
		<div class="dialog-btn btnContainer" data-align="center" data-valign="center">
			<button type="button" class="btn--secondary dialog--cancel${settings.text.btnClass ? ` ${settings.text.btnClass}` : ''}" data-size="medium"><span>${settings.text.cancelBtn}</span></button>
			<button type="button" class="btn--primary dialog--done${settings.text.btnClass ? ` ${settings.text.btnClass}` : ''}" data-size="medium"><span>${settings.text.doneBtn}</span></button>
		</div>
	</div>
</section>`);

	function closeDialog(event) {
		const $target = $(event.currentTarget);
		const $dialog = $target.closest('.dialog');
		const isCancel = $target.is('.dialog--cancel');
		const isDone = $target.is('.dialog--done');

		$dialog.remove();

		if (isDone && typeof settings.done === 'function') {
			settings.done();
		}

		if (isCancel && typeof settings.cancel === 'function') {
			settings.cancel();
		}
	}

	template.one('click', '.dialog-btn > *', closeDialog);
	$('body').append(template);
	template.one('click', '.dialog-closeBtn', (e) => {
		const $target = $(e.currentTarget);
		const $dialog = $target.closest('.dialog');
		$dialog.remove();
	})
};

$.lightbox = function (options) {
	const defaults = {
		target: '',
		closeClear: null
	};
	const settings = $.extend({}, defaults, options);
	const $target = $(settings.target);
	const $closeBtn = $target.find('.lightbox-closeBtn');
	function clearBox() {
		$target.removeAttr('data-opened');
		$('body').removeAttr('data-noScroll');
		if (settings.closeClear) {
			settings.closeClear()
		}
	}

	if ($target.length) {
		$target.attr('data-opened', true);
		$('body').attr('data-noScroll', true);
		$closeBtn.one('click', clearBox);
	}
};

$.fn.lightbox = function (options) {
	const defaults = {
		target: '',
		closeClear: null
	};
	let isClean = false
	const settings = $.extend({}, defaults, options);
	const outSide = (e, target, lightbox) => {
		e.stopPropagation();

		if (!$(target)[0].contains(e.target) && !$(lightbox).find('.lightbox-container')[0].contains(e.target) && !isClean) {
			isClean = true
			$(lightbox).removeAttr('data-opened');
			$('body').removeAttr('data-noScroll');
		}
	}

	this.on('click', function (event) {
		event.preventDefault();
		const $target = settings.target || $(this).attr('href') || $(this).data('lightbox');
		const overLayerClose = $($target).attr('over-layer-close') === 'true' ? true : false

		$.lightbox({
			target: $target,
			closeClear: settings.closeClear
		});

		if (overLayerClose) {
			isClean = false
			settings.closeClear = null
			$(document).off('click').on('click', (e) => outSide(e, this, $target))
		}
	});

	return this;
};

// resize
/**
 *
 */
function tableViewport() {
	let isReadyDrag;
	let isReadyScroll;
	let prevClientX = 0;
	let prevElementWidth = 0;
	const mouseAction = {
		down: function (event) {
			const viewport = $(this).width();
			const table = $(this).find('table').outerWidth();
			isReadyScroll = table > viewport;

			isReadyDrag = isReadyScroll;
			prevClientX = event.clientX;

			// console.log(isReadyDrag);
		},
		move: function (event) {
			if (isReadyDrag) {
				event.preventDefault();
				const currentClientX = event.clientX;

				$(this)[0].scrollLeft += (currentClientX - prevClientX) * -0.3;
			}
		},
		up: function (event) {
			isReadyDrag = false;
		}
	};
	const actions = {
		init: function (element) {
			$(element).on('mousedown', mouseAction.down).on('mousemove', mouseAction.move).on('mouseup', mouseAction.up);
		},
		resize: (entries) => {
			entries.forEach((entry) => {
				const $target = $(entry.target);
				const viewport = parseInt(entry.contentRect.width);
				const table = parseInt($target.find('table').outerWidth());
				const isReadyScroll = table > viewport;

				requestAnimationFrame(() => {
					$target.attr('data-scroll', isReadyScroll);
					prevElementWidth = viewport;
				});
			});
		}
	};

	$('.tableViewport').each(function (i, element) {
		actions.init(element);
		elementResizeObserver(element, actions.resize);
	});
}

// resize
/**
 * 表頭滾動至頂
 */
function tableHeadSticky() {
	function table(entries) {
		entries.forEach((entry) => {
			const $table = $(entry.target);
			const compareHeight = $('.floatFundCompare').length > 0 ? $('.floatFundCompare').outerHeight() : 0;
			const floatNavHeight = $('.floatNav').length > 0 ? $('.floatNav').outerHeight() : 0;
			const headerHeight = $('header').length > 0 ? $('header').height() : 0;
			const tableViewport = $table.closest('.tableViewport').length == 0;
			const tableHeight = entry.contentRect.height;
			const viewport = $(window).innerHeight() - (headerHeight + compareHeight + floatNavHeight);
			const isSticky = tableHeight > viewport && tableViewport;

			if (isSticky) {
				$table.find('.fundListTable-head').addClass('fundListTable-sticky');
				$table.find('.fundListTable-group').addClass('fundListTable-sticky');
				$table.find('.fundTable-head').addClass('fundTable-sticky');
				$table.find('.fundTable-group').addClass('fundTable-sticky');
			} else {
				$table.find('.fundListTable-head').removeClass('fundListTable-sticky');
				$table.find('.fundListTable-group').removeClass('fundListTable-sticky');
				$table.find('.fundTable-head').removeClass('fundTable-sticky');
				$table.find('.fundTable-group').removeClass('fundTable-sticky');
			}
		});
	}

	$('table').each(function (i, element) {
		elementResizeObserver(element, table);
	});
}

function inputTextFocus() {
	const $input = $('.inputText');
	const $floatNav = $('.floatNav');
	const actions = {
		focus: function (event) {
			const $target = $(event.target);
			const datePickerTarget = $target.hasClass('flatpickr-input');
			const datePickerActive = $target.hasClass('active');
			const mobile = mobileCheck();

			if (datePickerActive) return;

			if (datePickerTarget) {
				const datePicker = $target[0]._flatpickr;
				$target[0].scrollIntoView({ block: 'center' });
				setTimeout(() => {
					datePicker.open();
				}, 300);
			} else {
				$target[0].scrollIntoView({ block: 'nearest' });
			}

			if (mobile) {
				requestAnimationFrame(function () {
					$floatNav.css('opacity', '0');
				});
			}
		},
		blur: function (event) {
			requestAnimationFrame(function () {
				$floatNav.removeAttr('style');
			});
		}
	};

	$input.on('focus', actions.focus).on('blur', actions.blur);
}

function loadingClose() {
	$('.loading').remove();
}

