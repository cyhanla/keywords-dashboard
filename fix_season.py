import re

with open('enhanced_dashboard.html', 'r') as f:
    content = f.read()

# 旧的代码模式
old_code = '''    // 计算距离旺季
    const season = d.season;
    const now = new Date();
    const currentMonth = now.getMonth() + 1;
    let peakMonth, daysToPeak;
    
    switch(season) {
        case 'spring': peakMonth = 3; break;
        case 'summer': peakMonth = 6; break;
        case 'autumn': peakMonth = 9; break;
        case 'winter': peakMonth = 12; break;
        default: peakMonth = currentMonth;
    }
    
    if (currentMonth <= peakMonth) {
        daysToPeak = (peakMonth - currentMonth) * 30;
    } else {
        daysToPeak = ((12 - currentMonth) + peakMonth) * 30;
    }
    
    document.getElementById('daysToPeak').textContent = `${daysToPeak} 天`;
    
    // 当前阶段
    const phaseMap = {
        'spring': '春季预热期',
        'summer': '夏季旺季',
        'autumn': '秋季准备期',
        'winter': '冬季高峰期',
        'all': '全年稳定期'
    };
    document.getElementById('seasonPhase').textContent = phaseMap[season] || '平稳期';'''

# 新的代码
new_code = '''    // 计算距离旺季和当前阶段（基于实际月份和趋势）
    const season = d.season;
    const now = new Date();
    const currentMonth = now.getMonth() + 1;
    let peakMonth, daysToPeak, phaseText;
    
    // 根据关键词类型和当前月份智能判断阶段
    switch(season) {
        case 'winter': // 冬季词：手套、围巾、冷帽
            peakMonth = 12;
            if (currentMonth >= 11 || currentMonth <= 1) {
                phaseText = currentMonth === 12 ? '🔥 冬季高峰期' : '❄️ 冬季旺季';
                daysToPeak = currentMonth <= 1 ? (1 - currentMonth) * 30 : 0;
            } else if (currentMonth >= 2 && currentMonth <= 4) {
                phaseText = '📉 冬季收尾期（下降中）';
                daysToPeak = ((12 - currentMonth) + 11) * 30;
            } else {
                phaseText = '💤 夏季淡季';
                daysToPeak = ((12 - currentMonth) + 11) * 30;
            }
            break;
            
        case 'summer': // 夏季词：防晒、遮阳帽
            peakMonth = 6;
            if (currentMonth >= 5 && currentMonth <= 7) {
                phaseText = currentMonth === 6 ? '🔥 夏季高峰期' : '☀️ 夏季旺季';
                daysToPeak = 0;
            } else if (currentMonth >= 3 && currentMonth <= 4) {
                phaseText = '📈 夏季预热期（上升中）';
                daysToPeak = (6 - currentMonth) * 30;
            } else if (currentMonth >= 8 && currentMonth <= 10) {
                phaseText = '📉 夏季收尾期（下降中）';
                daysToPeak = ((12 - currentMonth) + 5) * 30;
            } else {
                phaseText = '💤 冬季淡季';
                daysToPeak = ((12 - currentMonth) + 5) * 30;
            }
            break;
            
        default:
            phaseText = '📊 全年稳定';
            daysToPeak = 0;
    }
    
    // 根据实际趋势进一步细化
    if (d.growth > 15 && !phaseText.includes('高峰')) {
        phaseText += ' 📈 快速上升';
    } else if (d.growth < -15) {
        phaseText = phaseText.replace('期', '下降期');
    }
    
    document.getElementById('daysToPeak').textContent = daysToPeak > 0 ? `${daysToPeak} 天` : '当前就是';
    document.getElementById('seasonPhase').textContent = phaseText;'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('enhanced_dashboard.html', 'w') as f:
        f.write(content)
    print('Fixed seasonal logic')
else:
    print('Pattern not found')
