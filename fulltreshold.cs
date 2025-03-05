        public byte FullThreshold(byte paciente_viu, TMatExame[] matExame, int idPto)
        {
            byte resp = 0;
            switch (paciente_viu)
            {
                case 1:
                    if (matExame[idPto].Atenuacao == 0)
                    {
                        matExame[idPto].Atenuacao = -1;
                        matExame[idPto].Status = '=';
                        resp = 1;
                        break;
                    }
                    matExame[idPto].UltAtenNaoVista = matExame[idPto].Atenuacao;
                    if (matExame[idPto].primeiro == true)
                    {
                        matExame[idPto].primeiro = false;
                        matExame[idPto].UltAtenVista = Constantes.dbMin;
                        matExame[idPto].NCruzou = 0;
                        matExame[idPto].Delta = Constantes.bigdelta;
                        matExame[idPto].Atenuacao = matExame[idPto].Atenuacao - matExame[idPto].Delta;
                        if (matExame[idPto].Atenuacao <= 0)
                            matExame[idPto].Atenuacao = 0;
                        matExame[idPto].Status = '+';
                        resp = 0;
                        break;
                    }
                    if (matExame[idPto].Status == '-')
                    {
                        matExame[idPto].NCruzou++;
                        matExame[idPto].Delta = Constantes.smalldelta;
                        if (matExame[idPto].NCruzou >= 2)
                        {
                            matExame[idPto].Status = '=';
                            matExame[idPto].Atenuacao = (matExame[idPto].UltAtenNaoVista + matExame[idPto].UltAtenVista) / 2;
                            resp = 1;
                            break;
                        }
                        else
                        {
                            matExame[idPto].Atenuacao = matExame[idPto].Atenuacao - matExame[idPto].Delta;
                            if (matExame[idPto].Atenuacao <= 0)
                                matExame[idPto].Atenuacao = 0;
                            matExame[idPto].Status = '+';
                            resp = 0;
                            break;
                        }
                    }
                    matExame[idPto].Atenuacao = matExame[idPto].Atenuacao - matExame[idPto].Delta;
                    if (matExame[idPto].Atenuacao <= 0)
                        matExame[idPto].Atenuacao = 0;
                    matExame[idPto].Status = '+';
                    resp = 0;
                        break;
                 case 2:
                    matExame[idPto].UltAtenVista = matExame[idPto].Atenuacao;
                    if (matExame[idPto].primeiro == true)
                    {
                        matExame[idPto].primeiro = false;
                        matExame[idPto].NCruzou = 0;
                        matExame[idPto].UltAtenNaoVista = Constantes.dbMax;
                        matExame[idPto].Delta = Constantes.bigdelta;
                        matExame[idPto].Atenuacao = matExame[idPto].Atenuacao + matExame[idPto].Delta;
                        if (matExame[idPto].Atenuacao >= 40)
                            matExame[idPto].Atenuacao = 40;
                        matExame[idPto].Status = '-';
                        resp = 0;
                        break;
                    }
                    if (matExame[idPto].Status == '+')
                    {
                        matExame[idPto].NCruzou++;
                        matExame[idPto].Delta = Constantes.smalldelta;
                        if (matExame[idPto].NCruzou >= 2)
                        {
                            matExame[idPto].Status = '=';
                            matExame[idPto].Atenuacao = (matExame[idPto].UltAtenNaoVista + matExame[idPto].UltAtenVista) / 2;
                            resp = 1;
                            break;
                        }
                        else
                        {
                            matExame[idPto].Atenuacao = matExame[idPto].Atenuacao + matExame[idPto].Delta;
                            if (matExame[idPto].Atenuacao >= 40)
                                matExame[idPto].Atenuacao = 40;
                            matExame[idPto].Status = '-';
                            resp = 0;
                            break;
                        }
                    }
                    matExame[idPto].Atenuacao = matExame[idPto].Atenuacao + matExame[idPto].Delta;
                    if (matExame[idPto].Atenuacao >= 40)
                        matExame[idPto].Atenuacao = 40;
                    matExame[idPto].Status = '-';
                    resp = 0;
                    break;
            }
            if (matExame[idPto].Status == '=')
            {
                Dados.gContIgual++;
            }   
        //         if ((Dados.gFlutuacao) && (!Dados.DadosExame.LF) && (Dados.gExame[idPto].SF) && Dados.LimQuad == false)
        //             setLimiarFlutuacao(matExame, idPto);
        //     }
        //     if ((resp == 1) && (!Dados.DadosExame.LF)&& (!Dados.DadosExame.ThrRel) && (!Dados.LimQuad))
        //         VerifyFalseNegative();
        //     return resp;
        // }