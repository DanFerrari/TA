            int UV = 0, AT = 0, UNV = 0, NC = 0, Delta = 0, viu = 0, Dbig, Dsmall;
            bool primeiro = true;
            char status;
            bool limiarok;
            double limiar = 0F;
            Color cor = Color.Red;
            Estimulo.TempoExposicao = 200;
            Estimulo.TamanhoIII();
            Fixacao.FixacaoDiamante(dictionary);
            limiarok = false;
            Dbig = 3;
            Dsmall = 2;
            labelAviso.Text = dictionary.getTranslation("Calculando Limiar Foveal (dB)");
            while (limiarok == false && Dados.stop == false)
            {
                await ForcarAtencao();
                await Task.Delay(1500);
                status = ' ';
                primeiro = true;
                AT = 25;
                while (status != '=' && Dados.stop == false)
                {
                    switch (status)
                    {
                        case ' ':
                            cor = Color.Red;
                            break;
                        case '+':
                            cor = Color.Blue;
                            break;
                        case '-':
                            cor = Color.Green;
                            break;
                    }
                    if (Dados.DadosExame.Programa == Constantes.Cinetico)
                    {
                        PlotaLimFovCin(AT, cor);
                    }
                    else
                    {
                        PlotaLimFov(AT, cor);
                    }
                    if (trackmode == "A")
                    {
                        string avisoatual = labelAviso.Text;
                        Color coravisoatual = labelAviso.ForeColor;
                        while ((!pupilacentrada) && (!Dados.stop) && (!Dados.Paused))
                        {
                            labelAviso.ForeColor = Color.Red;
                            labelAviso.Text = "Pupila Descentrada!!";
                            await Hardware.Bipar(5);
                            await Task.Delay(200);
                        }
                        labelAviso.ForeColor = coravisoatual;
                        labelAviso .Text = avisoatual;
                    }
                    Dados.gEsperaHardware = true;
                    viu = await SistemaProjecao.TestaEstimuloRCFix(new Coordenada(0, 0), (double)AT, dictionary);
                    Dados.gEsperaHardware = false;
                    if (trackmode != "D")
                    {
                        lbDiametroPupila.Text = diametropupila.ToString("#0.0") + " mm";
                    }
                    else
                    {
                        lbDiametroPupila.Text = Dados.DadosExame.DiamPup.ToString("#0.0") + " mm";
                    }
                    await Task.Delay(400);
                    switch (viu)
                    {
                        case 1:
                            if (AT <= 0)
                            {
                                AT = -1;
                                status = '=';
                                break;
                            }
                            UNV = AT;
                            if (primeiro == true)
                            {
                                primeiro = false;
                                NC = 0;
                                UV = 0;
                                Delta = Dbig;
                                AT = AT - Delta;
                                status = '+';
                                break;
                            }
                            if (status == '-')
                            {
                                NC++;
                                Delta = Dsmall;
                                if (NC >= 2)
                                {
                                    status = '=';
                                    AT = (UV + UNV) / 2;
                                    break;
                                }
                                else
                                {
                                    AT = AT - Delta;
                                    status = '+';
                                    break;
                                }
                            }
                            else
                            {
                                AT = AT - Delta;
                                status = '+';
                                break;
                            }

                        case 2:
                            UV = AT;
                            if (primeiro == true)
                            {
                                primeiro = false;
                                NC = 0;
                                UNV = 40;
                                Delta = Dbig;
                                AT = AT + Delta;
                                status = '-';
                                break;
                            }
                            if (status == '+')
                            {
                                NC++;
                                Delta = Dsmall;
                                if (NC >= 2)
                                {
                                    status = '=';
                                    AT = (UV + UNV) / 2;
                                    break;
                                }
                                else
                                {
                                    AT = AT + Delta;
                                    status = '-';
                                    break;
                                }
                            }
                            else
                            {
                                AT = AT + Delta;
                                status = '-';
                                break;
                            }
                    }
                    if (AT > 45)
                        AT = 45;
                }
                if (Dados.stop == false)
                {
                    limiar = AT;
                    if (Dados.DadosExame.Programa == Constantes.Cinetico)
                    {
                        PlotaLimFovCin(AT, Color.Black);
                    }
                    else
                    {
                        PlotaLimFov(AT, Color.Black);
                    }
                    if (Dados.DadosExame.Programa != Constantes.Cinetico)
                    {
                        short[] limiaresbase = new short[Dados.DadosExame.limiaresBaseRef.Length];
                        limiaresbase = fn.OrdenaDecrescente(Dados.DadosExame.limiaresBaseRef);
                        double somamaiores = 0;
                        double medialimiares = 0;
                        for (int i = 0; i < 4; i++)
                            somamaiores = somamaiores + limiaresbase[i];
                        medialimiares = somamaiores / 4;
                        if (limiar < medialimiares)
                            if (MessageBox.Show(dictionary.getTranslation("Limiar foveal = ") + Convert.ToInt16(limiar) + dictionary.getTranslation(" dB\n Abaixo do esperado! (") + medialimiares + dictionary.getTranslation(" dB)\nSim para Novo Exame \nNão para continuar assim mesmo"), dictionary.getTranslation("Atenção"), MessageBoxButtons.YesNo, MessageBoxIcon.Information) == DialogResult.Yes)
                                limiarok = false;
                            else
                                limiarok = true;
                        else
                            limiarok = true;
                    }
                    else
                    {
                        limiarok = true;
                    }
                }
            }
            Dados.DadosExame.LimiarFoveal = limiar;
            lbLimarFoveal.Text = "Limiar Foveal: " + Dados.DadosExame.LimiarFoveal.ToString();
            Fixacao.FixacaoCentral(dictionary);
            await Task.Delay(800);
        }
https://chatgpt.com/share/67b62af0-6c50-8012-851b-cd940996f5f0